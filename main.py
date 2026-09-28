import json
import os

prompts = [
    {
        "title": "얼굴 외형과 체형에 따른 옷 디자인 및 브랜드 매칭",
        "content": "사용자의 얼굴형(달걀형, 각진형, 라운드형 등)과 체형(체격, 키, 어깨 너비) 데이터를 분석하여 최적의 패션 스타일링 및 옷 디자인을 추천하고, 이에 어울리는 브랜드(컨템포러리, 캐주얼, 스트릿 등)를 매칭해주는 AI 프롬프트입니다.",
        "category": "페르소나",
        "favorite": True,
        "views": 0
    },
    {
        "title": "남성 패션 블로그 프롬프트 매니저",
        "content": "남성 트렌드 패션, 체형별 스타일링 팁, 계절별 착장 추천을 주제로 작성하는 전문 패션 블로거 페르소나입니다. SEO에 최적화된 서론-본론-결론 구조와 클릭률을 높이는 블로그 제목 3가지를 함께 생성합니다.",
        "category": "텍스트 생성",
        "favorite": False,
        "views": 0
    },
    {
        "title": "ADER ERROR 브랜드 광고 영상 스크립트",
        "content": "아더에러(ADER ERROR)의 4명 디자이너(건축가, 그래픽 디자이너, 요리사, 의류 디자이너)의 일상 속 영감 탐색 과정을 교차 연출로 보여주며, 마지막에 '당신이 무심코 지나친 일상의 결함이, 우리의 가장 완벽한 예술이 됩니다.'라는 핵심 카피를 강조하는 30초 광고 영상 스크립트 프롬프트입니다.",
        "category": "영상 생성",
        "favorite": True,
        "views": 0
    }
]

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

def show_menu():
    print("\n==========================================")
    print("      나만의 프롬프트 관리 시스템 (v1.0)")
    print("==========================================")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록 보기")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리 (토글)")
    print("7. 즐겨찾기 목록 보기")
    print("8. [보너스] JSON 저장 및 불러오기")
    print("9. [보너스] 카테고리별 Markdown 내보내기")
    print("0. 종료")
    print("==========================================")

def add_prompt():
    print("\n[ 프롬프트 추가 ]")
    while True:
        title = input("제목을 입력하세요: ").strip()
        if title:
            break
        print("❌ 제목은 빈 값일 수 없습니다. 다시 입력해 주세요.")
        
    while True:
        content = input("내용을 입력하세요: ").strip()
        if content:
            break
        print("❌ 내용은 빈 값일 수 없습니다. 다시 입력해 주세요.")

    print("\n카테고리를 선택하세요:")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"{idx}) {cat}")
    
    cat_choice = input("선택 (1~6 또는 직접 입력): ").strip()
    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(CATEGORIES):
        category = CATEGORIES[int(cat_choice) - 1]
    elif cat_choice:
        category = cat_choice
    else:
        category = "기타"

    new_item = {
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0
    }
    prompts.append(new_item)
    print(f"✅ '{title}' 프롬프트가 성공적으로 추가되었습니다!")

def show_list(items=None, title_label="전체 프롬프트 목록"):
    target_list = items if items is not None else prompts
    print(f"\n[ {title_label} ]")
    if not target_list:
        print("등록된 프롬프트가 없습니다.")
        return

    for idx, item in enumerate(target_list, 1):
        fav_icon = "⭐" if item.get("favorite") else "  "
        views = item.get("views", 0)
        print(f"{idx}. [{item['category']}] {item['title']} {fav_icon} (조회수: {views})")
    print(f"\n총 {len(target_list)}개의 프롬프트")

def view_by_category():
    print("\n[ 카테고리별 조회 ]")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"{idx}) {cat}")
    
    choice = input("조회할 카테고리 번호를 입력하세요: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(CATEGORIES)):
        print("❌ 올바른 카테고리 번호가 아닙니다.")
        return

    selected_cat = CATEGORIES[int(choice) - 1]
    filtered = [p for p in prompts if p["category"] == selected_cat]
    show_list(filtered, f"'{selected_cat}' 카테고리 결과")

def search_prompt():
    print("\n[ 프롬프트 검색 ]")
    keyword = input("검색어를 입력하세요: ").strip().lower()
    if not keyword:
        print("❌ 검색어를 입력해야 합니다.")
        return

    results = [p for p in prompts if keyword in p["title"].lower() or keyword in p["content"].lower()]
    show_list(results, f"'{keyword}' 검색 결과")

def show_detail():
    show_list()
    if not prompts:
        return

    choice = input("\n상세히 볼 프롬프트 번호를 입력하세요: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print("❌ 존재하지 않는 번호입니다.")
        return

    item = prompts[int(choice) - 1]
    item["views"] = item.get("views", 0) + 1

    fav_str = "⭐" if item.get("favorite") else "❌"
    print("\n" + "─" * 40)
    print(f"제목     : {item['title']}")
    print(f"카테고리 : {item['category']}")
    print(f"즐겨찾기 : {fav_str}")
    print(f"조회수   : {item['views']}")
    print("─" * 40)
    print("내용:")
    print(item["content"])
    print("─" * 40)

def toggle_favorite():
    show_list()
    if not prompts:
        return

    choice = input("\n즐겨찾기를 설정/해제할 프롬프트 번호: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print("❌ 올바른 번호가 아닙니다.")
        return

    target = prompts[int(choice) - 1]
    target["favorite"] = not target.get("favorite", False)
    status = "추가" if target["favorite"] else "해제"
    print(f"✅ '{target['title']}' 프롬프트가 즐겨찾기 목록에서 {status}되었습니다!")

def show_favorites():
    fav_list = [p for p in prompts if p.get("favorite")]
    show_list(fav_list, "즐겨찾기 프롬프트 목록")

def save_to_json(filename="prompts.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=4)
        print(f"✅ 성공적으로 '{filename}' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"❌ 저장 중 오류 발생: {e}")

def load_from_json(filename="prompts.json"):
    global prompts
    if not os.path.exists(filename):
        print(f"❌ '{filename}' 파일이 존재하지 않습니다.")
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        print(f"✅ '{filename}' 파일에서 데이터를 불러왔습니다.")
    except Exception as e:
        print(f"❌ 불러오기 중 오류 발생: {e}")

def export_to_markdown():
    md_content = "# 📝 내 프롬프트 컬렉션\n\n"
    grouped = {}
    for p in prompts:
        cat = p["category"]
        grouped.setdefault(cat, []).append(p)

    for cat, items in grouped.items():
        md_content += f"## 📁 {cat}\n\n"
        for item in items:
            fav = "⭐ " if item.get("favorite") else ""
            md_content += f"### {fav}{item['title']}\n"
            md_content += f"- **조회수:** {item.get('views', 0)}\n"
            md_content += f"```text\n{item['content']}\n```\n\n"

    filename = "exported_prompts.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ 카테고리별 프롬프트가 '{filename}' 파일로 내보내졌습니다!")

def main():
    while True:
        show_menu()
        choice = input("선택할 메뉴 번호를 입력하세요: ").strip()

        if choice == "1":
            add_prompt()
        elif choice == "2":
            show_list()
        elif choice == "3":
            view_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            toggle_favorite()
        elif choice == "7":
            show_favorites()
        elif choice == "8":
            print("1) 파일로 저장하기 | 2) 파일에서 불러오기")
            sub = input("선택: ").strip()
            if sub == "1":
                save_to_json()
            elif sub == "2":
                load_from_json()
        elif choice == "9":
            export_to_markdown()
        elif choice == "0":
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            print("\n❌ 잘못된 입력입니다. 0~9 사이의 숫자를 입력해주세요.")

if __name__ == "__main__":
    main()