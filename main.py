import flet as ft
from datetime import datetime
import requests


# Настройки шрифтов
ft.Page.fonts = {
    "Montserrat": '/Montserrat.ttf'
}


def fetch_news(selected_tags=None):
    try:
        # Базовые параметры запроса
        params = [("skip", 0), ("limit", 100)]

        # Добавляем теги, если они выбраны
        if selected_tags:
            for tag in selected_tags:
                params.append(("tags", tag))

        # Отправляем запрос с параметрами
        response = requests.get("https://black-bears-service.onrender.com/api/v1/news", params=params)
        response.raise_for_status()
        news_data = response.json()
        return prepare_news(news_data)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе новостей: {e}")
        return []

def prepare_news(news_data):
    prepared_news = []
    for news in news_data:
        # Укорачиваем текст для краткого содержания
        short_content = news["content"][:100] + "..." if len(news["content"]) > 100 else news["content"]
        prepared_news.append({
            "title": news["title"],
            "date": datetime.fromisoformat(news["created_at"]),  # Преобразуем строку в datetime
            "content": short_content,  # Краткий текст
            "full_content": news["content"],  # Полный текст
            "image": news["image_url"],  # URL изображения
        })
    return prepared_news

def news_card(page, news):
    show_full_content = False

    # Текстовый элемент для отображения контента
    content_text = ft.Text(
        news["content"],  # По умолчанию показываем краткий текст
        color="#FFFFFF",
        size=14,
    )

    # Кнопка для переключения текста
    button = ft.ElevatedButton(
        "Читать полностью",
        color="#FFFFFF",
        bgcolor="#095644",
        style=ft.ButtonStyle(padding=10),
    )

    # Функция для переключения текста
    def toggle_content(e):
        nonlocal show_full_content
        show_full_content = not show_full_content

        # Обновляем текст
        content_text.value = (
            news["full_content"] if show_full_content else news["content"]
        )

        # Обновляем текст кнопки
        button.text = "Свернуть" if show_full_content else "Читать полностью"

        # Обновляем страницу
        page.update()

    # Привязываем обработчик к кнопке
    button.on_click = toggle_content

    # Возвращаем карточку с фиксированной шириной
    return ft.Container(
        content=ft.Card(
            color="#2E363E",
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Image(src=news['image'], width=800, height=200, fit=ft.ImageFit.COVER, border_radius=10),
                        ft.Text(news['title'], color="#FFFFFF", size=20, weight=ft.FontWeight.W_600),
                        ft.Text(news['date'].strftime("%d.%m.%Y"), color="#707070", size=12),
                        content_text,  # Отображаем текст
                        button,  # Отображаем кнопку
                    ],
                    spacing=10,
                ),
            ),
        ),
        width=800,  # Ограничиваем ширину карточки
        alignment=ft.alignment.center,  # Центрируем карточку
    )


# Класс для сообщений
class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

# Класс для отображения сообщений в чате
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold", color=ft.colors.WHITE),
                    ft.Text(message.text, selectable=True, color=ft.colors.WHITE),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def fetch_tags():
    try:
        response = requests.get("https://black-bears-service.onrender.com/api/v1/news/tags/")
        response.raise_for_status()
        res = response.json()
        return res
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе тегов: {e}")
        return []

# Основной макет страницы
def main(page: ft.Page):
    page.appbar = header
    page.bottom_appbar = footer
    page.title = "Черные Медведи - Новости"
    page.bgcolor = "#1C1B19"
    page.font_family = "Montserrat"

    # Новостная лента
    news_feed = ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    tags = fetch_tags()
    selected_tags = []

    # Чекбоксы для выбора тегов
    tag_checkboxes = ft.Column(
        scroll=ft.ScrollMode.AUTO
    )

    # Функция для обновления тегов
    def update_tags():
        nonlocal tags
        tags = fetch_tags()  # Загружаем теги с сервера
        tag_checkboxes.controls = [
            ft.Checkbox(
                label=tag['name'],
                value=tag['name'] in selected_tags,  # Сохраняем состояние выбранных тегов
                on_change=lambda e, tag=tag: update_selected_tags(e, tag)
            ) for tag in tags
        ]
        page.update()

    # Функция для обновления выбранных тегов
    def update_selected_tags(e, tag):
        if e.control.value:
            selected_tags.append(tag['name'])
        else:
            selected_tags.remove(tag['name'])
        update_news()

    # Обновление новостей с учетом выбранных тегов
    def update_news(e=None):
        news_feed.controls.clear()
        news_feed.controls.extend([news_card(page, news) for news in fetch_news(selected_tags)])
        
        page.update()

    # Функция для обновления новостей и тегов
    def refresh_data(e=None):
        update_tags()  # Обновляем теги
        update_news()  # Обновляем новости

    # Кнопка для обновления новостей
    refresh_button = ft.IconButton(
        icon=ft.icons.REFRESH,
        tooltip="Обновить новости",
        on_click=refresh_data,  # Привязываем функцию обновления
        icon_color="#FFFFFF",
        bgcolor="#095644",
    )


    # Заголовок новостной ленты с кнопкой обновления
    news_header = ft.Row(
        controls=[
            ft.Text("Новости", size=24, color="#FFFFFF", weight=ft.FontWeight.W_600),
            refresh_button,  # Добавляем кнопку обновления
            tag_checkboxes,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Размещаем текст и кнопку по краям
    )

    # Контейнер для новостной ленты
    news_container = ft.Container(
    content=ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Новости", size=24, color="#FFFFFF", weight=ft.FontWeight.W_600),
                        refresh_button,  # Добавляем кнопку обновления
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Размещаем текст и кнопку по краям
                ),
                padding=ft.padding.only(bottom=20),  # Отступ снизу
            ),
            ft.Container(
                content=tag_checkboxes,
                padding=ft.padding.only(bottom=20),  # Отступ снизу
            ),
            news_feed,  # Новостная лента
        ],
        scroll=ft.ScrollMode.AUTO,  # Добавляем скроллинг для всей ленты
        expand=True,
    ),
    padding=ft.padding.symmetric(horizontal=30, vertical=20),
    alignment=ft.alignment.center,  # Центрируем содержимое контейнера
    width=800,  # Ограничиваем ширину контейнера
    )

    # Обновляем новости при загрузке страницы
    refresh_data()

    # Чат
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # Поле для ввода нового сообщения
    new_message = ft.TextField(
        hint_text="Введите сообщение...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=lambda e: send_message_click(e),
        color=ft.colors.WHITE,
        bgcolor="#1C1B19",
        border_color=ft.colors.WHITE,
    )

    # Функция для отправки сообщения
    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    # Функция для обработки входящих сообщений
    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.WHITE54, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # Диалоговое окно запроса имени
    join_user_name = ft.TextField(
        label="Введите имя чтобы присоединиться к чату",
        autofocus=True,
        on_submit=lambda e: join_chat_click(e),
        color=ft.colors.WHITE,
        bgcolor='#1C1B19',
        border_color=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.WHITE),
    )
    welcome_dlg = ft.AlertDialog(
        open=False,  # По умолчанию окно закрыто
        modal=True,
        title=ft.Text("Добро пожаловать!", color=ft.colors.WHITE),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=lambda e: join_chat_click(e))],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#1C1B19",
    )

    page.overlay.append(welcome_dlg)

    # Функция для присоединения к чату
    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Имя не может быть пустым"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            welcome_dlg.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ", color=ft.colors.WHITE)
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} присоединился к чату.",
                    message_type="login_message",
                )
            )
            page.update()

    # Функция для обработки изменения вкладки
    def on_tab_change(e):
        if e.control.selected_index == 1:  # Если выбрана вкладка "Обсуждение"
            if not page.session.get("user_name"):  # Если имя пользователя не задано
                welcome_dlg.open = True
                page.update()



    # Вкладки для переключения между новостями и комментариями
    tabs = ft.Tabs(
    selected_index=0,
    on_change=on_tab_change,  # Обработчик изменения вкладки
    tabs=[
        ft.Tab(
            text="Новости",
            content=ft.Container(
                content=news_container,
                alignment=ft.alignment.center,  # Центрируем содержимое
                expand=True,
            ),
        ),
        ft.Tab(
            text="Обсуждение",
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=chat,
                            border=ft.border.all(1, ft.colors.WHITE),
                            border_radius=5,
                            padding=10,
                            height=368,  # Высота окошка чата
                            width=800,   # Ширина окошка чата
                            expand=False,
                            bgcolor="#1C1B19",
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        content=new_message,
                                        height=50,  # Высота панели ввода сообщения
                                        expand=True,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.SEND_ROUNDED,
                                        tooltip="Отправить сообщение",
                                        on_click=send_message_click,
                                        icon_color=ft.colors.WHITE,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            padding=10,
                            width=600,  # Ширина панели ввода сообщения
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Центрирование всей колонки
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,  # Центрирование содержимого контейнера
                expand=True,
            ),
        ),
    ],
    expand=True,
    )

    # Добавляем вкладки на страницу
    page.add(
        ft.Container(
            content=tabs,
            padding=ft.padding.symmetric(horizontal=40),
            alignment=ft.alignment.center,
            width=page.width,
            expand=True,
        )
    )

# ниже уже футер и хедер
news_text = ft.Text("Новости", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
men = ft.Text("Мужская команда", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
women = ft.Text("Женская команда", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
address = ft.Row([ft.Icon(name=ft.Icons.LOCATION_PIN, color="#2E363E"),
                  ft.Text("г. Санкт-Петербург, ул. Политехническая, д. 27 (Спортивный комплекс «Политехник»)",
                          font_family="Montserrat", color='#FFFFFF', size=12, weight=ft.FontWeight.W_300,
                          style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE))])
email = ft.Row([ft.Icon(name=ft.Icons.EMAIL, color="#2E363E"),
                ft.Text("sskblackbears@spbstu.ru", font_family="Montserrat", color='#FFFFFF', size=12,
                        weight=ft.FontWeight.W_300)])
title = ft.Row([email, address], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

footer = ft.BottomAppBar(
    bgcolor="#131211",
    height=60,
    content=ft.Row(
        controls=[
            ft.Image(src='/polytech.png'),
            ft.Image(src='/asb.png'),
            ft.Row([
                ft.Text("Мы в соцсетях: ", font_family="Montserrat", weight=ft.FontWeight.W_300,
                        size=14, color='#776E67'),
                ft.CupertinoButton(content=ft.Image(src='/vk.png'), padding=5, url='https://vk.com/blackbears_mbasket'),
                ft.CupertinoButton(content=ft.Image(src='/youtube.png'), padding=5, url='https://www.youtube.com/@blackbears-polytech3931'),
                ft.CupertinoButton(content=ft.Image(src='/tg.png'), padding=5, url='https://t.me/bearsbasketball'), ],
                alignment=ft.MainAxisAlignment.END)
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY),
)

header = ft.AppBar(
        toolbar_height=95,
        leading_width=700,
        bgcolor="#1C1B19",
        leading=ft.Row(
            [
             ft.CupertinoButton(content=men, bgcolor='#095644', width=161, height=42, padding=2),
             ft.CupertinoButton(content=women, bgcolor='#095644', width=161, height=42, padding=2),
             ft.CupertinoButton(content=news_text, bgcolor='#095644', width=161, height=42, padding=2)],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY),

        center_title=False,
        title=title,
        actions=[
        ],
        elevation_on_scroll=0
    )

# ft.app(target=main, view=ft.WEB_BROWSER, host='192.168.51.208', port=80)
ft.app(target=main, view=ft.WEB_BROWSER, port=80)