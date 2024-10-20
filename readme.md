# bluedef

![bluedef.png](bluedef.png)

bluedef is a lightweight library designed to simplify Bluetooth GATT (Generic Attribute Profile) integration. It provides predefined UUIDs and company identifiers as constants to ensure easy access from ```C```, ```C++```, and ```Rust``` environments, especially in embedded systems where bundling YAML files is not practical.

This library aims to improve readability and maintainability in your Bluetooth projects by offering standardized, auto-generated headers or modules containing necessary Bluetooth identifiers.

## Features

- **Predefined Constants for UUIDs and Identifiers**
Access Bluetooth company IDs, service UUIDs, characteristic UUIDs, and more as constants.

- **Support for Multiple Languages**
Generate code in C, C++, and Rust with template-based outputs.

- **Minimal and Lightweight**
Avoid dependency on YAML files at runtime. All relevant data is converted into code during compilation.

- **Auto-Generated Headers**
The library automatically generates consistent headers or modules from YAML configurations.

## Getting Started

Copy curated output file to your project. That's it!

**Or, if you want to transpile by yourself..**

```
```