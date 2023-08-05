from plone.namedfile.browser import DisplayFile
from plone.namedfile.browser import Download
from plone.namedfile.utils import set_headers


def download_set_headers(self, file):
    # With filename None, set_headers will not add the download headers.
    if not self.filename:
        self.filename = getattr(file, "filename", None)
        if self.filename is None:
            self.filename = self.fieldname
            if self.filename is None:
                self.filename = "file.ext"
    set_headers(file, self.request.response, filename=self.filename)


# We would usually let the patched method call the original method,
# but with set_headers the original method is really small and has not changed
# in ages.  Do keep the original, in case someone needs it.
Download._orig_set_headers = Download.set_headers
Download.set_headers = download_set_headers

# List of mimetypes that we allow to display inline.
# This is mostly to avoid XSS (Cross Site Scripting).
# We especially do not want image/svg+xml, text/html, application/javascript.
# If a Manager has a use case for displaying those inline, there are other ways to create them,
# for example in the ZMI or via the Resource Registries or Theming control panel.
# ATContentTypes allows PDF and a few old MS Office formats to display inline.
# But I think most browsers always ask what you want to do for each mimetype,
# and you can let it remember your answer.
# So: a few image mimetypes are likely enough here.
# Note: a tag like `<img src="example.svg" />` loading an image/svg+xml mimetype will show up fine.
# But when you visit example.svg as url, you will get a download.
ALLOWED_INLINE_MIMETYPES = [
    "image/gif",
    # The mimetypes registry lists several for jpeg 2000:
    "image/jp2",
    "image/jpeg",
    "image/jpeg2000-image",
    "image/jpeg2000",
    "image/jpx",
    "image/png",
    "image/webp",
    "image/x-icon",
    "image/x-jpeg2000-image",
    "text/plain",
]

# Make the allowed list available on the class.
# Then subclasses can override this.
DisplayFile.allowed_inline_mimetypes = ALLOWED_INLINE_MIMETYPES
DisplayFile._orig_set_headers = DisplayFile.set_headers


def display_set_headers(self, file):
    if hasattr(file, "contentType"):
        mimetype = file.contentType
        if mimetype not in self.allowed_inline_mimetypes:
            # Let the Download view handle this.
            super(DisplayFile, self).set_headers(file)
    self._orig_set_headers(file)


DisplayFile.set_headers = display_set_headers
