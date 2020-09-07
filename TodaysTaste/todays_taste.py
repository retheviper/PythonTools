import PySimpleGUI as sg

sg.theme('SystemDefaultForReal')

def create_button(text: str):
    return sg.Button(text, size = (10, 5))

chinese_menu: str = '중식'
japanese_menu: str  = '일식'
meat_menu: str = '고기'
ramen_menu: str = '라면'
else_menu: str = '기타'
korean_menu: str = '한식'
chicken_menu: str = '치킨'
dessert_menu: str = '분식'
close_menu: str = '닫기'

initial_layer: list = [
    [create_button(chinese_menu), create_button(japanese_menu), create_button(meat_menu)],
    [create_button(ramen_menu), create_button(close_menu), create_button(else_menu)],
    [create_button(korean_menu), create_button(chicken_menu), create_button(dessert_menu)]
    ]

chinese_layer: list = [
    [create_button('탕수육'), create_button('깐풍기'), create_button('칠리새우')],
    [create_button('짬뽕'), create_button(close_menu), create_button('사천탕수육')],
    [create_button('짜장면'), create_button('유린기'), create_button('꿔바로우')]
    ]

japanese_layer: list = [
    [create_button('초밥'), create_button('돈부리'), create_button('참치홰')],
    [create_button('소바'), create_button(close_menu), create_button('오코노미야끼')],
    [create_button('라멘'), create_button('장어덮밥'), create_button('우동')]
    ]

meat_layer: list = [
    [create_button('삼겹살'), create_button('갈비'), create_button('갈매기살')],
    [create_button('항정살'), create_button(close_menu), create_button('목살')],
    [create_button('가브리살'), create_button('등심'), create_button('안심')]
    ]

ramen_layer: list = [
    [create_button('비빔면'), create_button('신라면'), create_button('짜왕')],
    [create_button('너구리'), create_button(close_menu), create_button('불닭볶음면')],
    [create_button('삼양라면'), create_button('진라면'), create_button('안성탕면')]
    ]

else_layer: list = [
    [create_button('스테이크'), create_button('파스타'), create_button('훈제오리')],
    [create_button('햄버거'), create_button(close_menu), create_button('쌀국수')],
    [create_button('피자'), create_button('만두'), create_button('커리')]
    ]

korean_layer: list = [
    [create_button('냉면'), create_button('설렁탕'), create_button('닭도리탕')],
    [create_button('간장게장'), create_button(close_menu), create_button('김치찌개')],
    [create_button('낙지'), create_button('불고기백반'), create_button('곱창')]
    ]

chicken_layer: list = [
    [create_button('BBQ 양념치킨'), create_button('BBC 뿌링클'), create_button('네네치킨 파닭')],
    [create_button('굽네치킨'), create_button(close_menu), create_button('네네치킨 스노잉')],
    [create_button('교촌치킨'), create_button('KFC'), create_button('파파이스')]
    ]
    
dessert_layer: list = [
    [create_button('떡볶이'), create_button('순대'), create_button('빙수')],
    [create_button('오뎅'), create_button(close_menu), create_button('보쌈')],
    [create_button('케이크'), create_button('빵'), create_button('푸딩')]
    ]

main_window = sg.Window('Today\'s Taste!', initial_layer)

if __name__ == '__main__':
    while True:             
        event, values = main_window.read()
        if event in (sg.WIN_CLOSED, close_menu):
            break
        elif event in (chinese_menu):
            main_window = sg.Window(chinese_menu, chinese_layer)
        elif event in (japanese_menu):
            main_window = sg.Window(japanese_menu, japanese_layer)
        elif event in (meat_menu):
            main_window = sg.Window(meat_menu, meat_layer)
        elif event in (ramen_menu):
            main_window = sg.Window(ramen_menu, ramen_layer)
        elif event in (else_menu):
            main_window = sg.Window(else_menu, else_layer)
        elif event in (korean_menu):
            main_window = sg.Window(korean_menu, korean_layer)
        elif event in (chicken_menu):
            main_window = sg.Window(chicken_menu, chicken_layer)
        elif event in (dessert_menu):
            main_window = sg.Window(dessert_menu, dessert_layer)
        else:
            sg.popup('결정했습니다: ' + event)

    main_window.close()