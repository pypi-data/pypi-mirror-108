# Package Cake 🎂

**Package Cake** is a simple utility that takes your package and turns it
into cake 🍰.

## Installation

```bash
python -m pip install packagecake
```

## Bake a Package Cake

```bash
python -m packagecake bake [your package name]
```

```bash
>> python -m packagecake bake requests
🍰
```

## PyPI Package Cake Stats

In addition to single package baking, **Package Cake** can also bake all
the packages in PyPI and provide the total of each type of cake.

```bash
>> python -m packagecake stats
------------------------------
|  PyPI Package Cake Stats   |
------------------------------
|🍩 - Donut         | 153821 |
------------------------------
|🧁 - Cupcake       | 77134  |
------------------------------
|🍰 - Shortcake     | 38769  |
------------------------------
|🎂 - Birthday Cake | 20632  |
------------------------------
|🥮 - Moon Cake     | 17793  |
------------------------------
|🍥 - Fish Cake     | 352    |
------------------------------
```
