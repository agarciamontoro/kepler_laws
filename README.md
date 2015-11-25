# Leap Motion project

## Introduction
This repository contains the Leap Motion project developed for the course **Nuevos Paradigmas de Interacción** at the University of Granada, Spain.

The final goal is to simulate the classical game of *las chapas*, letting the user to interact with the computer through the movement of its own hands.

### Current state
By now, just a first recognition and interaction phase has been implemented. The functionality now is simple: the scene has just a ball that changes its colour when it is touched.

## Instalation
The project is coded in Python, using the Leap Motion driver and the OpenGL library. The required dependencies are the following:

1. **Python2**
2. **Leap-Motion-Driver**
3. **Leap-Motion-SDK**
4. **Python2-OpenGL**
5. **Python2-pygame**
6. **Python2-pillow**
7. **Python2-enum34**

The most common distributions have all the library packages needed, but maybe the Leap Motion driver and SDK are not in the repositories. However, it is easy to download them from the [Download](https://developer.leapmotion.com/downloads) section of Leap Motion web page.


The [Python API](https://developer.leapmotion.com/documentation/python/index.html) could also be useful if some error appear.

If the Python OpenGL library is not in your distribution repository, use the package manager **pip** to install them.

### Arch Linux example
Arch Linux has all required packages in the official -and AUR- repositories. To install Python and OpenGL, execute the following order:
```
$> pacman -S python2 python2-opengl python2-pygame
```

[leap-motion-driver](https://aur.archlinux.org/packages/leap-motion-driver) and [leap-motion-sdk](https://aur.archlinux.org/packages/leap-motion-sdk) packages are not in the official repository but in the Arch User Repository. To install them, just build the packages manually or use a package manager like `pacaur`:

```
$> pacaur -S leap-motion-driver leap-motion-sdk
```

Caution! leap-motion-sdk throws an error if the pkg-build is not edited. You have to add `${pkgdir}` in the following lines
```
install -D -m644 "/usr/lib/Leap/Leap.py" "${pkgdir}/usr/lib/python2.7/site-packages/Leap.py"
install -D -m644 "/usr/lib/Leap/LeapPython.so" "${pkgdir}/usr/lib/python2.7/site-packages/LeapPython.so"
```

They have to look like this:
```
install -D -m644 "${pkgdir}/usr/lib/Leap/Leap.py" "${pkgdir}/usr/lib/python2.7/site-packages/Leap.py"
install -D -m644 "${pkgdir}/usr/lib/Leap/LeapPython.so" "${pkgdir}/usr/lib/python2.7/site-packages/LeapPython.so"
```

## Execution and usage
Connect the Leap Motion, start the daemon -with `sudo leapd`-, and execute the following order:
```
$> python2 main.py
```

You will see a tutorial like the following:

![Primera escena](Screenshots/01.png)

Follow the tutorial step by step and you will get to the real program!s

![02](Screenshots/02.png)

![03](Screenshots/03.png)

![04](Screenshots/04.png)

When you finish the tutorial, you can start playing with the ball and with its colors. Try to touch it with one hand, the other, or even both of them!

## First assignment
### Problem considered
The final goal is to improve and make more real the interaction with the computer through the use of the Leap Motion device and its developer API.

As a first assignment, we decided to create a scene in which the hands were realistically created and where we could test an interaction proof of concept.

The first idea that came to our heads was to become a Jedi. We wanted the Leap to detect our hand gestures and use the Force to move objects throughout the scene. However, this idea, as it is already implemented by someone else, was changed by a simpler game concept: the old classical *las chapas*.

### Solutions proposed

The first decision we made was the language and graphic library we wanted to use. Initially, we wanted to use Unreal Engine or Unity3D, as its graphic power and ease to use are greater than OpenGL. However, we chose this later option: our computers have low performance and a Linux+OpenGL setup is more appropriate for us; furthermore, Windows and Unreal or Unity are privative and need higher computing power.

Then, we decided which language to use: we needed a multi-platform language in which we could program fast. We did not worry about the computing performance: some milliseconds more or less were not critical. Python fulfill all these requirements and, furthermore, we had a Python code implementing the basic OpenGL structure.

With the language and libraries chosen, we started the project.

We found the first difficulty at the very beginning: the drawing of the hands was not trivial. We spent a lot of time dealing with the hand structure provided by Leap Motion and, overall, with the OpenGL code.

The hand bone structure is simple and easy to use: all the important points are given as three-dimensional vectors in milimiters and the direction of the bones are provided as normalized vectors. We tried to visualize the bones as cylinders that were first drawn in the origin and then were rotated and translated. The translation was easily achieved, but we spent too much time dealing with the rotation code and decided to try a simpler solution: as all the bone junctions were given as points in the space, we just had to draw lines between each pair of them. All our rotation problems vanished.

When we had the hand representation nearly finished, we started to make the interaction code. As a first idea, that was the one we finally implemented, we decided to draw a ball in the space and to let the user touch it and see its color changing.

The implementation of this code was straightforward; we did not have too much problems with it, as just some distances had to be measured and some colors had to be changed. However, when we had all the program working, we realized that the visualization was poor: we needed the user to understand where his/her hands were. We needed to add some reference that could make more real the positioning of the hands in the virtual world: the shadows were the solution!

A simple but powerful shadow was implemented: the hands were just projected in the XZ plane with a gray color. Later, we improved the solution by changing the shadow relative size depending on the Y coordinate.

When the program was finished, we made a simple tutorial that explained how to use the program. Furthermore, we chose to implement Leap gestures to advance throughout the tutorial: the user has to make a key tap gesture in order to get to the next step.

The gesture was easily implemented with the Gesture interface of the API.

## References
* **GUI.py**: the basic OpenGL functions -init, camera, projection and view settings- in this file are adapted from this [@analca3](https://github.com/analca3)'s repository: [Triodo de Frenet](https://github.com/analca3/TriedroFrenet_Evoluta).
* **LeapDriver.py**: the basic structure of this file is taken from the [Hello World tutorial](https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html).
* **Billiard cloth**: the texture used is taken from [](http://www.photos-public-domain.com/2012/08/14/kelly-green-microfiber-cloth-fabric-texture/)
