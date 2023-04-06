# Quiron

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter](https://img.shields.io/twitter/follow/luctstt.svg?label=Follow&style=social)](https://twitter.com/iluzioDev)

---

<video width="100%" controls="controls" src="https://user-images.githubusercontent.com/45295283/211917624-f9b2433e-9d37-4c20-97c5-2fb3fb93b326.mp4">Your browser does not support the HTML5 Video element.</video>

## Introduction

Quiron is a Python package that provides hand detection, gesture recognition, and finger counting, so developers can easily integrate hand tracking and gesture recognition functionality into their applications, allowing for more natural and intuitive user interactions.

Quiron leverages the powerful [Mediapipe framework](https://mediapipe.dev/), which uses machine learning models to accurately detect hands in images and video streams. Once hands are detected, Quiron provides a range of functionalities for recognizing different gestures, such as thumbs up or peace sign, as well as counting the number of fingers that are raised.

## Features

- Hand Recognition
- Hand Movement Detection
- Hand Gesture Recognition
- Finger Counting

## Installation

```console
pip install quiron
```

## API

### Hand Recognition

```{eval-rst}
.. autofunction:: quiron.count_fingers
```

```{eval-rst}
.. autofunction:: quiron.detect_gestures
```

```{eval-rst}
.. autofunction:: quiron.gestures.distance
```

```{eval-rst}
.. autofunction:: quiron.gestures.raised
```

```{eval-rst}
.. autofunction:: quiron.gestures.sideways
```

## Maintainers

<table>
  <tr>
    <td align="center"><a href="https://github.com/iluzioDev"><img src="https://avatars.githubusercontent.com/u/45295283?v=4" width="100px;" alt="IluzioDev"/><br /><sub><b>IluzioDev</b></sub></a><br />💻</td>
  </tr>
</table>

## License ⚖️

Distributed under the MIT License. [Click here](LICENSE.md) for more information.

---

<div align="center">
	<b>
		<a href="https://www.npmjs.com/package/get-good-readme">File generated with get-good-readme module</a>
	</b>
</div>
