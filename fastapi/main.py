from fastapi import FastAPI
from fastapi.responses import FileResponse
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
current_path = os.path.dirname(os.path.abspath(__file__))
static_files_path = os.path.join(current_path, "static")



app = FastAPI()
app.mount("/static", StaticFiles(directory=static_files_path), name="static")

def truncate_text(text, length):
    if len(text) > length:
        truncated_text = text[:length] + "..."
    else:
        truncated_text = text
    return truncated_text




@app.get("/")
def main():
    html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>메인 페이지</title>
        </head>
        <body>
            <h1>목록을 선택하세요</h1>
            <p>
                <a href="/series">Series 목록</a><br>
                <a href="/movies">Movies 목록</a>
            </p>
        </body>
        </html>
    '''
    return FileResponse('main_page.html')



@app.get("/series")
def total_chart():
    series_list = pd.read_csv("./disney_series.csv")
    
    
    
    # HTML 테이블 생성
    html_table = "<head>\n<link rel='stylesheet' type='text/css' href='/static/styles.css'>\n</head>"
    html_table += "<title>disney_series</title>\n"
    html_table += "<div class='title'>디즈니 시리즈 목록</div>"
    html_table += "<table>\n"
    html_table += "<tr>\n"
    html_table += "<th>번호</th>\n"
    html_table += "<th>포스터</th>\n"
    html_table += "<th>제목</th>\n"
    html_table += "<th>개봉연도</th>\n"
    html_table += "<th>시즌</th>\n"
    html_table += "<th>장르</th>\n"
    html_table += "<th>줄거리</th>\n"
    html_table += "<th>배우</th>\n"
    html_table += "<th>러닝타임</th>\n"
    html_table += "</tr>\n"

    for index, row in series_list.iterrows():
        truncated_overview = truncate_text(row["overview"], 100)
        html_table += "<tr>\n"
        html_table += f"<td>{index+1}</td>\n"
        html_table += f"<td><img src='{row['img']}' alt='Album Image' width='300' height='150'></td>\n"
        html_table += f"<td>{row['title']}</td>\n"
        html_table += f"<td>{row['open']}</td>\n"
        html_table += f"<td>{row['series']}</td>\n"
        html_table += f"<td>{row['genre']}</td>\n"
        html_table += f"<td>{truncated_overview}</td>\n"
        html_table += f"<td>{row['actors']}</td>\n"
        html_table += f"<td>{row['runtime']}</td>\n"
        html_table += "</tr>\n"

    html_table += "</table>"

    # HTML 파일 생성
    with open('disney_series.html', 'w') as file:
        file.write(html_table)

    
    return FileResponse('disney_series.html')


        
        
@app.get("/movies")
def disney_movie():
    movie_list = pd.read_csv("./disneymovies.csv")
    
    
    
    # HTML 테이블 생성
    html_table = "<head>\n<link rel='stylesheet' type='text/css' href='/static/styles.css'>\n</head>"
    html_table += "<title>disney_movies</title>\n"
    html_table += "<div class='title'>디즈니 영화 목록</div>"
    html_table += "<table>\n"
    html_table += "<tr>\n"
    html_table += "<th>번호</th>\n"
    html_table += "<th>포스터</th>\n"
    html_table += "<th>제목</th>\n"
    html_table += "<th>개봉연도</th>\n"
    html_table += "<th>장르</th>\n"
    html_table += "<th>줄거리</th>\n"
    html_table += "<th>감독</th>\n"
    html_table += "<th>배우</th>\n"
    html_table += "<th>러닝타임</th>\n"
    html_table += "</tr>\n"

    for index, row in movie_list.iterrows():
        truncated_overview = truncate_text(row["overview"], 100)
        html_table += "<tr>\n"
        html_table += f"<td>{index+1}</td>\n"
        html_table += f"<td><img src='{row['img']}' alt='Album Image' width='300' height='150'></td>\n"
        html_table += f"<td>{row['title']}</td>\n"
        html_table += f"<td>{row['open']}</td>\n"
        html_table += f"<td>{row['genre']}</td>\n"
        html_table += f"<td>{truncated_overview}</td>\n"
        html_table += f"<td>{row['director']}</td>\n"
        html_table += f"<td>{row['actor']}</td>\n"
        html_table += f"<td>{row['runtime']}</td>\n"
        html_table += "</tr>\n"

    html_table += "</table>"

    # HTML 파일 생성
    with open('disney_movie.html', 'w') as file:
        file.write(html_table)

    
    return FileResponse('disney_movie.html')



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)