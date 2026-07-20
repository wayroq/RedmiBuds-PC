import asyncio
import threading
import ctypes
from bleak import BleakScanner

class BluetoothManager:
    def __init__(self, on_battery_update, on_status_update):
        self.on_battery_update = on_battery_update
        self.on_status_update = on_status_update
        
        # Определяем язык Windows (1049 = Русский)
        try:
            self.is_ru = ctypes.windll.kernel32.GetUserDefaultUILanguage() == 1049
        except Exception:
            self.is_ru = False
            
        self.running = False
        self.thread = None
        self.scanner = None
        self.loop = None
        self.last_left = -1
        self.last_right = -1
        self.last_case = -1

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.scanner and self.loop:
            asyncio.run_coroutine_threadsafe(self.scanner.stop(), self.loop)

    def _run_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._scan_forever())

    async def _scan_forever(self):
        self.on_status_update("Поиск наушников (BLE)..." if self.is_ru else "Searching for earbuds (BLE)...")
        
        def callback(device, adv):
            if "Redmi" in str(device.name) or "Buds" in str(device.name):
                # Google Fast Pair service UUID
                gfps_uuid = "0000fe2c-0000-1000-8000-00805f9b34fb"
                if gfps_uuid in adv.service_data:
                    data = adv.service_data[gfps_uuid]
                    self._parse_gfps_data(data)

        self.scanner = BleakScanner(callback)
        await self.scanner.start()
        
        while self.running:
            await asyncio.sleep(1)
            
        await self.scanner.stop()

    def _parse_gfps_data(self, data):
        # We parse the raw bytes based on real-world logs.
        if len(data) >= 13:
            # For Redmi Buds 6, the battery data is located at offsets 10, 11, 12
            left_byte = data[10]
            right_byte = data[11]
            case_byte = data[12]

            l_val = left_byte & 0x7F if left_byte != 0xFF else -1
            r_val = right_byte & 0x7F if right_byte != 0xFF else -1
            c_val = case_byte & 0x7F if case_byte != 0xFF else -1
            
            # If case is 0 or 127, it might be an invalid reading
            if c_val == 0 or c_val == 127:
                c_val = -1

            if l_val != self.last_left or r_val != self.last_right or c_val != self.last_case:
                self.last_left = l_val
                self.last_right = r_val
                self.last_case = c_val
                
                self.on_battery_update(l_val, r_val, c_val)
                self.on_status_update("Подключено (BLE)" if self.is_ru else "Connected (BLE)")
