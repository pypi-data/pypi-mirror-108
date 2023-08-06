=====
Usage
=====

To use Koodous in a project::

    from koodous.api import Koodous

    koodous = Koodous('INSERT_YOUR_TOKEN')
    apk = koodous.apk('INSERT_APK_SHA256')
    print(apk)

Get your token on your `Koodous profile <https://koodous.com/settings/profile>`_ and find the Koodous apks checksums in
`<https://koodous.com/apks>`_.


There are more code examples in the `examples folder <https://github.com/Koodous/python-sdk/tree/master/examples>`_.
