Changelog
=========


1.3 (2021-06-01)
----------------

- Moved ``CHANGES.rst`` to main directory and add a ``version.txt`` there.
  This makes it easier to check that you have the correct version when you use the zip download
  from https://plone.org/security/hotfix/20210518.
  This file is cached, so you might get an earlier version.
  Check the sha1 or md5 checksum to be sure.

- Define a set ``ALLOWED_UNDERSCORE_NAMES`` with allowed names.
  This currently contains ``__name__``, ``_`` and ``_authenticator``.
  This makes it easier for projects to add a name in a patch if this is really needed.
  Be sure you know what you are doing if you override this.

- Allow accessing a single underscore ``_``.
  After the merge of the hotfix, Zope allows this to fix a test failure.
  Seems wise to allow it in the hotfix too.

- Allow accessing ``_authenticator`` from plone.protect in more cases.
  The previous version did this for a traverse class, and now also for a traverse function.


1.2 (2021-05-19)
----------------

- Allow accessing ``_authenticator`` from plone.protect.
  It fixes a NotFound error when submitting a PloneFormGen form,
  see `issue 229 <https://github.com/smcmahon/Products.PloneFormGen/pull/229>`_.
  Should solve similar cases as well.

- Fixed the expressions patch.
  It unintentionally changed the behavior of the ``TrustedBoboAwareZopeTraverse`` class as well.
  Most importantly, it let this class use ``restrictedTraverse``, so it did unwanted security checks:
  this class is used for expressions in trusted templates on the file system.
  Needed for all Plone versions, except 4.3 when it does not have the optional ``five.pt`` package.
  One test is: login as Editor and go to the ``@@historyview`` of a page.
  If you get an ``Unauthorized`` error, you should upgrade to the new version.
  If you are unsure: install this version.


1.1 (2021-05-18)
----------------

- Allow using ``__name__`` in untrusted expressions.
  The previous expressions patch was too strict.
  This may be needed in case you have templates that use `__name__`.
  This does not happen often, but one example is the ``caching-controlpanel`` view,
  which with the previous version may give a 404 NotFound error.
  In some Plone versions browser views are affected (Plone 4.3 with five.pt, 5.0, 5.1, 5.2.0-5.2.2).
  In all Plone versions skin or through-the-web templates are affected.
  When you see more NotFound errors than normal, you should install this new version.
  If you are unsure: install this version.


1.0 (2021-05-18)
----------------

- Initial release
