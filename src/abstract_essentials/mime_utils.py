"""
abstract_essentials.mime_utils
================================
MIME type registry and media-category detection.
"""
import os

MIME_TYPES = {
    'image': {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
        '.gif': 'image/gif', '.bmp': 'image/bmp', '.tiff': 'image/tiff',
        '.webp': 'image/webp', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
        '.heic': 'image/heic', '.psd': 'image/vnd.adobe.photoshop',
        '.raw': 'image/x-raw', '.apng': 'image/apng', '.heif': 'image/heif',
        '.jp2': 'image/jp2', '.jxl': 'image/jxl', '.eps': 'application/postscript',
        '.ai': 'application/postscript',
    },
    'video': {
        '.mp4': 'video/mp4', '.webm': 'video/webm', '.ogg': 'video/ogg',
        '.mov': 'video/quicktime', '.avi': 'video/x-msvideo', '.mkv': 'video/x-matroska',
        '.flv': 'video/x-flv', '.wmv': 'video/x-ms-wmv', '.3gp': 'video/3gpp',
        '.mpeg': 'video/mpeg', '.mpg': 'video/mpg', '.m4v': 'video/x-m4v',
        '.f4v': 'video/x-f4v', '.asf': 'video/x-ms-asf', '.vob': 'video/dvd',
        '.m2ts': 'video/mp2t', '.mts': 'video/mp2t',
    },
    'audio': {
        '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.flac': 'audio/flac',
        '.aac': 'audio/aac', '.ogg': 'audio/ogg', '.m4a': 'audio/mp4',
        '.opus': 'audio/opus', '.aif': 'audio/x-aiff', '.aiff': 'audio/x-aiff',
        '.amr': 'audio/amr', '.mid': 'audio/midi', '.midi': 'audio/midi',
        '.wma': 'audio/x-ms-wma', '.mka': 'audio/x-matroska',
    },
    'document': {
        '.pdf': 'application/pdf', '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.odt': 'application/vnd.oasis.opendocument.text', '.txt': 'text/plain',
        '.rtf': 'application/rtf', '.md': 'text/markdown', '.markdown': 'text/markdown',
        '.tex': 'application/x-tex', '.log': 'text/plain', '.json': 'application/json',
        '.xml': 'application/xml', '.yaml': 'application/x-yaml', '.yml': 'application/x-yaml',
        '.ini': 'text/plain', '.cfg': 'text/plain', '.toml': 'application/toml',
        '.csv': 'text/csv', '.tsv': 'text/tab-separated-values',
        '.epub': 'application/epub+zip', '.mobi': 'application/x-mobipocket-ebook',
        '.azw': 'application/vnd.amazon.ebook',
        '.pages': 'application/x-iwork-pages-sffpages',
        '.numbers': 'application/x-iwork-numbers-sffnumbers',
        '.key': 'application/x-iwork-keynote-sffkey',
    },
    'presentation': {
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.odp': 'application/vnd.oasis.opendocument.presentation',
    },
    'spreadsheet': {
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ods': 'application/vnd.oasis.opendocument.spreadsheet',
        '.csv': 'text/csv', '.tsv': 'text/tab-separated-values',
    },
    'data_science': {
        '.parquet': 'application/x-parquet', '.avro': 'application/avro',
        '.hdf5': 'application/x-hdf5', '.h5': 'application/x-hdf5',
        '.pickle': 'application/octet-stream', '.npy': 'application/x-npy',
        '.npz': 'application/x-npz', '.ipynb': 'application/x-ipynb+json',
        '.sqlite': 'application/x-sqlite3', '.db': 'application/x-sqlite3',
    },
    'code': {
        '.py': 'text/x-python', '.java': 'text/x-java-source', '.c': 'text/x-c',
        '.cpp': 'text/x-c++', '.h': 'text/x-c', '.hpp': 'text/x-c++',
        '.js': 'application/javascript', '.cjs': 'application/javascript',
        '.mjs': 'application/javascript', '.jsx': 'application/javascript',
        '.ts': 'application/javascript', '.tsx': 'application/typescript',
        '.rb': 'text/x-ruby', '.php': 'application/x-php', '.go': 'text/x-go',
        '.rs': 'text/rust', '.swift': 'text/x-swift', '.kt': 'text/x-kotlin',
        '.sh': 'application/x-shellscript', '.bash': 'application/x-shellscript',
        '.ps1': 'application/x-powershell', '.sql': 'application/sql',
        '.yml': 'application/x-yaml', '.coffee': 'text/coffeescript', '.lua': 'text/x-lua',
        '.css': 'text/css', '.scss': 'text/x-scss', '.sass': 'text/x-sass',
        '.less': 'text/x-less', '.html': 'text/html', '.htm': 'text/html',
        '.vue': 'text/x-vue', '.svelte': 'text/x-svelte',
        '.graphql': 'application/graphql', '.gql': 'application/graphql',
        '.dockerfile': 'text/x-dockerfile', '.makefile': 'text/x-makefile',
        '.sol': 'text/x-solidity',
    },
    'three_d': {
        '.obj': 'model/obj', '.stl': 'model/stl', '.glb': 'model/gltf-binary',
        '.gltf': 'model/gltf+json', '.fbx': 'application/octet-stream',
        '.usd': 'model/usd', '.usdz': 'model/vnd.usdz+zip',
        '.blend': 'application/x-blender',
    },
    'archive': {
        '.zip': 'application/zip', '.tar': 'application/x-tar',
        '.gz': 'application/gzip', '.tgz': 'application/gzip',
        '.bz2': 'application/x-bzip2', '.xz': 'application/x-xz',
        '.rar': 'application/vnd.rar', '.7z': 'application/x-7z-compressed',
        '.iso': 'application/x-iso9660-image', '.dmg': 'application/x-apple-diskimage',
        '.jar': 'application/java-archive', '.war': 'application/java-archive',
        '.whl': 'application/python-wheel', '.egg': 'application/python-egg',
        '.zpaq': 'application/x-zpaq',
    },
    'font': {
        '.ttf': 'font/ttf', '.otf': 'font/otf', '.woff': 'font/woff',
        '.woff2': 'font/woff2', '.eot': 'application/vnd.ms-fontobject',
    },
    'executable': {
        '.exe': 'application/vnd.microsoft.portable-executable',
        '.dll': 'application/vnd.microsoft.portable-executable',
        '.bin': 'application/octet-stream',
        '.deb': 'application/vnd.debian.binary-package',
        '.rpm': 'application/x-rpm', '.app': 'application/x-executable',
        '.ipa': 'application/x-itunes-ipa',
        '.apk': 'application/vnd.android.package-archive',
    },
    'geospatial': {
        '.geojson': 'application/geo+json',
        '.kml': 'application/vnd.google-earth.kml+xml',
        '.kmz': 'application/vnd.google-earth.kmz',
        '.shp': 'application/x-qgis-main-file',
        '.shx': 'application/x-qgis-shape-index', '.dbf': 'application/x-dbf',
        '.gpkg': 'application/geopackage+sqlite3', '.gpx': 'application/gpx+xml',
        '.tif': 'image/tiff', '.tiff': 'image/tiff', '.osm': 'application/xml',
        '.wkt': 'text/plain',
    },
    'pandas_data': {
        '.parquet': 'application/x-parquet', '.feather': 'application/x-feather',
        '.orc': 'application/x-orc', '.hdf': 'application/x-hdf',
        '.h5': 'application/x-hdf5', '.pickle': 'application/octet-stream',
        '.pkl': 'application/octet-stream', '.msgpack': 'application/x-msgpack',
        '.stata': 'application/x-stata', '.dta': 'application/x-stata',
        '.sas7bdat': 'application/x-sas-data', '.sav': 'application/x-spss-sav',
    },
}

# Category → set of extensions; mirrors the package-level MEDIA_TYPES.
MEDIA_TYPES = {category: set(mapping.keys()) for category, mapping in MIME_TYPES.items()}


def derive_media_type(obj):
    """Return the media category (e.g. 'image', 'video') for a path or extension."""
    ext = os.path.splitext(str(obj))[-1] or obj
    if ext:
        for typ, exts in MEDIA_TYPES.items():
            if ext in exts:
                return typ
    return None


def get_mime_type(obj):
    """Return the MIME string (e.g. 'image/png') for a path or extension, or None."""
    ext = os.path.splitext(str(obj))[-1].lower() or str(obj).lower()
    for mapping in MIME_TYPES.values():
        if isinstance(mapping, dict) and ext in mapping:
            return mapping[ext]
    return None


def make_key_map(dict_obj):
    """Build a category → set-of-keys map from a nested dict."""
    return {k: set(v.keys()) for k, v in dict_obj.items()}


__all__ = [
    "MIME_TYPES", "MEDIA_TYPES",
    "derive_media_type", "get_mime_type", "make_key_map",
]
