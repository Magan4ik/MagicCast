# Magic Cast

# Розгортування проекту

## Встановлення python
Завантажте та встановіть Python 3.10.10.
- Windows [Python3.10](https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe)
- Mac [Python3.10](https://www.python.org/ftp/python/3.10.10/python-3.10.10-macos11.pkg)

*При встановлені на Windows не забудьте натиснути "Add Python 3.10 to PATH".*

## Встановіть Git

- Windows [Git](https://github.com/git-for-windows/git/releases/download/v2.36.1.windows.1/Git-2.36.1-64-bit.exe)

## 📥 Клонування репозиторію

Спочатку потрібно завантажити код проєкту:
```bash
git clone https://github.com/Magan4ik/MagicCast.git
cd MagicCast
```

## 🐍 Створення віртуального середовища

Рекомендується використовувати віртуальне середовище для ізоляції залежностей:
```bash
python -m venv venv
```
Активуйте його:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

## 📦 Встановлення залежностей

Всі необхідні бібліотеки знаходяться у файлі `requirements.txt`. Встановіть їх за допомогою:
```bash
pip install -r requirements.txt
```

## 🚀 Запуск проєкту

```bash
python main.py
```
(Замість `main.py` вкажіть `map_editor.py`, щоб запустити редактор карти.)

Тепер ви готові працювати над проєктом! 🎉