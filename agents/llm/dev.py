import jurigged  # type: ignore

from app import app

def watch_and_reload():
    _ = jurigged.watch('.')
    app(debug=True)

if __name__ == '__main__':
    watch_and_reload()
    