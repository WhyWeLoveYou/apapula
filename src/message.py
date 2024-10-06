from bs4 import BeautifulSoup
from markdownify import markdownify as md

def extract_content(response, search_key):
    """
    Extracts content from the response based on the search_key found in the first cell of a table row.
    """
    soup = BeautifulSoup(response, 'html.parser')
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1 and cells[0].get_text(strip=True) == search_key:
            return cells[1].decode_contents()
    return None  # Return None if not found

def get_materi(response):
    return extract_content(response, "Isi Materi")

def get_title(response):
    soup = BeautifulSoup(response, 'html.parser')
    title_div = soup.find('div', class_='card-header')
    return title_div.get_text(strip=True) if title_div else "No Title Found"

def get_assignment(response):
    return extract_content(response, "Tugas Dari Guru")

def create_message(response, date, link):
    response = response.replace("`", "")
    materi = get_materi(response) or "Tidak Ada Materi"
    title = get_title(response)
    assignment = get_assignment(response) or "Tidak Ada Tugas"
    
    if len(materi) > 4096:
        materi = "Karakter materi melebihi batas pengiriman telegram, buka halaman materi dengan menekan judul materi untuk lebih lanjut."
    
    message = (
        f"{date}\n\n"
        f"[{title}]({link})\n{'=' * 20}\n"
        f"{md(materi)}\n{'=' * 20}\n"
        f"Tugas :\n{md(assignment)}"
    )
    
    # Clean up the message
    message = message.replace("`", "").replace(
        'Powered by [Froala Editor](https://www.froala.com/wysiwyg-editor?pb=1 "Froala Editor")', ""
    )

    return message
