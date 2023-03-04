import os
import re
import requests
from bs4 import BeautifulSoup

folder_path = r'S:\Temp\Upload'
output_file = '- video_info.txt'

# Open the output file for writing
with open(os.path.join(folder_path, output_file), 'w', encoding='utf-8') as f_out:

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('_encoded.mp4'):
            # Extract first 8 characters from the filename
            # video_id = file_name[:8]
            first_dash_pos = file_name.index("-")
            second_dash_pos = file_name.index("-", first_dash_pos + 1)
            video_id = file_name[:second_dash_pos]
            print(video_id)
            # Construct the search URL for Javlibrary.com
            search_url = f'https://www.javlibrary.com/tw/vl_searchbyid.php?keyword={video_id}'

            # Fetch the search results page
            response = requests.get(search_url)

            # Parse the HTML response and extract the required video information
            soup = BeautifulSoup(response.content, 'html.parser')

            # Check if there are multiple search results
            result_list = soup.find_all('div', {'class': 'video'})
            if len(result_list) > 1:
                # Find the first result with a matching ID
                for result in result_list:
                    result_id = result.find('div', {'class': 'id'}).text.strip()
                    if result_id.casefold() == video_id.casefold():
                        # Use this result
                        result_url = 'https://www.javlibrary.com/tw/' + result.find('a')['href']
                        result_response = requests.get(result_url)
                        break
                else:
                    # If no matching result is found, use the first result
                    result_url = 'https://www.javlibrary.com/tw/' + result_list[0].find('a')['href']
                    result_response = requests.get(result_url)
            else:
                # If there is only one search result, fetch the result page directly
                result_response = requests.get(search_url)

            # Parse the HTML response and extract the required video information
            result_soup = BeautifulSoup(result_response.content, 'html.parser')
            orgTitle = result_soup.find('h3', {'class': 'post-title text'}).text.strip()
            video_id = orgTitle.split(" ", 1)[0]
            video_title = orgTitle.split(" ", 1)[1]

            video_date = result_soup.find('div', {'id': 'video_date'})	

            # Find the element that contains the video cast
            cast_element = result_soup.find("div", {"id": "video_cast"})
            # Extract the video cast from the element and remove the first value
            video_cast = cast_element.text.strip().split("\n")[1:]            

            # Format the video cast by adding "#" in front of each name
            cast_list = []
            for name in video_cast:
                name = name.strip()
                if not name.startswith("("):
                    formatted_name = "#" + name.replace(" ", "\n#") + "\n"
                    cast_list.append(formatted_name)

            # Add a newline character at the end of the formatted video cast
            cast_list.append("\n")

            maker_id_element = result_soup.find("div", {"id": "video_maker"})
            video_maker = maker_id_element.text.strip()
            video_maker = video_maker.replace('\n', ' ')
            video_maker = video_maker.replace(' ', " #")

            label_id_element = result_soup.find("div", {"id": "video_label"})
            video_label = label_id_element.text.strip()
            video_label = video_label.replace('\n', ' ')
            video_label = video_label.replace(' ', " #")

            # Find the HTML element that contains the list of genres
            genres_div = result_soup.find('div', {'id': 'video_genres'})
            genre_spans = genres_div.find_all('span', {'class': 'genre'})
            genres = []
            for genre_span in genre_spans:
                genre = genre_span.find('a').text
                if genre not in ["薄馬賽克", "數位馬賽克"]:
                    genres.append(genre)                 

            # Add a "#" symbol in front of each genre
            genres = ["#" + genre for genre in genres]

            cover_url = 'https:' + result_soup.find('img', {'id': 'video_jacket_img'}).get('src')

            # Download the cover image
            cover_response = requests.get(cover_url)
            cover_file_path = os.path.join(folder_path, f'{video_id}.jpg')
            with open(cover_file_path, 'wb') as f:
                f.write(cover_response.content)

            #Output to text file
            f_out.write(f'{video_id} {video_title}\n')
            f_out.write("".join(cast_list))            
            f_out.write(f'{video_maker}\n')
            f_out.write(f'{video_label}\n')
            # Write the genres to a text file
            for genre in genres:
                f_out.write(genre+' ')
            f_out.write(f'#AK網友 \n')
            third_element = "-"+file_name.split("-")[2]
            if "-C" in third_element:
                f_out.write(f'#中文字幕\n')
            else:
                f_out.write(f'')
            f_out.write(f'👉🏼 @galaxyjj ❤️ 宇宙channel - AV谷 ❤️\n')
            f_out.write('\n\n')