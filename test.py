from pathlib import Path

# Отримати шлях до директорії static
static_directory = BASE_DIR.joinpath("src").joinpath("static")

# Перевірити, чи існує директорія static
if not static_directory.exists():
    # Якщо не існує, створити директорію
    static_directory.mkdir(parents=True, exist_ok=True)

# Монтувати статичні файли
app.mount("/static", StaticFiles(directory=static_directory), name="static")
