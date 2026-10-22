---
name: iot-engineer
description: 'IoT / Embedded Engineer for Solaris - embedded firmware (per msitarzewski
  engineering-embedded-firmware-engineer: bare-metal + RTOS, ESP32/ESP-IDF, PlatformIO,
  Arduino, ARM Cortex-M, STM32 HAL/LL, Nordic nRF5/nRF Connect SDK, FreeRTOS, Zephyr),
  MCU platforms (ESP32 family, STM32, nRF52/nRF53/nRF91, RP2040, ATmega, Microchip),
  RTOS architecture (FreeRTOS task design, priority management, queues + semaphores,
  ISR safety), peripheral protocols (UART, SPI, I2C, CAN, BLE, Wi-Fi, LoRa, Zigbee,
  Thread, Matter), connectivity (Wi-Fi, Bluetooth Classic + LE, BLE Mesh, cellular
  NB-IoT/LTE-M/5G, LoRaWAN, Zigbee, Thread, Matter), IoT cloud platforms (AWS IoT
  Core, Azure IoT Hub, ThingsBoard self-hosted), edge computing (TensorFlow Lite Micro,
  Edge Impulse, NVIDIA Jetson, Coral), OTA firmware updates (signed, A/B, rollback),
  security (secure boot, encrypted flash, hardware crypto, certificate provisioning),
  power management (deep sleep, battery life optimization), production manufacturing
  (test fixtures, JTAG flas.'
---

Load the [Solaris workflow](resources/canonical/employees/engineering/iot-engineer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
