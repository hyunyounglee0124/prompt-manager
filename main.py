import json
import os
from datetime import datetime

# ==========================================
# 1. 초기 데이터 및 전역 설정
# ==========================================
JSON_FILENAME = "prompts.json"
MD_FILENAME = "exported_prompts.md"

CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타"
]

DEFAULT_PROMPTS = [
    {
        "id": 1,
        "title": "얼굴 외형과 체형에 따른 옷 디자인 및 브랜드 매칭",
        "content": "사용자의 얼굴형(달걀형, 각진형, 라운드형 등)과 체형(체격, 키, 어깨 너비) 데이터를 분석하여 최적의 패션 스타일링 및 옷 디자인을 추천하고, 이에 어울리는 브랜드(컨템포러리, 캐주얼, 스트릿 등)를 매칭해주는 AI 프롬프트입니다.",
        "category": "페르소나",
        "favorite": True,
        "views": 0,
        "created_at": "2026-09-28 10:00:00"
    },
    {
        "id": 2,
        "title": "남성 패션 블로그 프롬프트 매니저",
        "content": "당신은 10년 경력의 남성 전문 패션 블로거입니다. 남성 트렌드 패션, 체형별 스타일링 팁, 계절별 착장 추천을 주제로 작성합니다. SEO에 최적화된 서론-본론-결론 구조와 클릭률을 높이는 블로그 제목 3가지를 함께 생성해주세요.",
        "category": "텍스트 생성",
        "favorite": False,
        "views": 0,
        "created_at": "2026-09-28 11:30:00"
    },
    {
        "id": 3,
        "title": "ADER ERROR 브랜드 광고 영상 스크립트",
        "content": "아더에러(ADER ERROR)의 4명 디자이너(건축가, 그래픽 디자이너, 요리사, 의류 디자이너)의 일상 속 영감 탐색 과정을 교차 연출로 보여주며, 마지막에 '당신이 무심코 지나친 일상의 결함이, 우리의 가장 완벽한 예술이 됩니다.'라는 핵심 카피를 강조하는 30초 광고 영상 스크립트 프롬프트입니다.",
        "category": "영상 생성",
        "favorite": True,
        "views": 0,
        "created_at": "2026-09-28 13:15:00"
    }
]

prompts = []

def load_data():
    global prompts
    if os.path.exists(JSON_FILENAME):
        try:
            with open(JSON_FILENAME, "r", encoding="utf-8") as f:
                prompts = json.load(f)
            print(f"📂 [알림] '{JSON_FILENAME}' 파일에서 {len(prompts)}개의 프롬프트를 불러왔습니다.")
        except Exception as e:
            print(f"⚠️ [경고] 데이터 로드 중 오류 발생: {e}. 기본 데이터를 사용합니다.")
            prompts = list(DEFAULT_PROMPTS)
    else:
        prompts = list(DEFAULT_PROMPTS)
        save_data(silent=True)

def save_data(silent=False):
    try:
        with open(JSON_FILENAME, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=4)
        if not silent:
            print(f"💾 [성공] 데이터가 '{JSON_FILENAME}'에 저장되었습니다.")
    except Exception as e:
        print(f"❌ [오류] 데이터 저장 실패: {e}")

def get_next_id():
    if not prompts:
        return 1
    return max(p.get("id", 0) for p in prompts) + 1

def format_prompt_row(idx, item):
    fav = "⭐" if item.get("favorite") else "  "
    category = f"[{item['category']}]".ljust(10)
    views = f"(조회수: {item.get('views', 0)})"
    return f"{idx:2d}. {fav} {category} {item['title']} {views}"

def show_menu():
    print("\n" + "=" * 52)
    print("      🚀 나만의 AI 프롬프트 관리 시스템 v2.0")
    print("=" * 52)
    print(" 1. ➕ 프롬프트 추가")
    print(" 2. 📋 전체 프롬프트 목록 보기")
    print(" 3. 📁 카테고리별 조회")
    print(" 4. 🔍 키워드 검색")
    print(" 5. 📖 프롬프트 상세 보기")
    print(" 6. ⭐ 즐겨찾기 설정/해제 (토글)")
    print(" 7. 🌟 즐겨찾기 모아보기")
    print(" 8. 🔥 인기 프롬프트 TOP 목록 (조회수 순)")
    print(" 9. 🛠️ 프롬프트 수정 / 삭제")
    print("10. 📄 Markdown 파일 내보내기")
    print(" 0. 🚪 종료")
    print("=" * 52)

def add_prompt():
    print("\n[ ➕ 새 프롬프트 추가 ]")
    while True:
        title = input("📌 제목 입력: ").strip()
        if title:
            break
        print("❌ 제목은 공백일 수 없습니다. 다시 입력해주세요.")
        
    while True:
        content = input("📝 프롬프트 내용 입력: ").strip()
        if content:
            break
        print("❌ 내용은 공백일 수 없습니다. 다시 입력해주세요.")

    print("\n🏷️ 카테고리 선택:")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"  {idx}. {cat}")
    
    cat_choice = input("👉 번호 선택 (또는 직접 입력): ").strip()
    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(CATEGORIES):
        category = CATEGORIES[int(cat_choice) - 1]
    elif cat_choice:
        category = cat_choice
    else:
        category = "기타"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_prompt = {
        "id": get_next_id(),
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
        "created_at": now_str
    }
    
    prompts.append(new_prompt)
    save_data(silent=True)
    print(f"\n✅ '{title}' 프롬프트가 성공적으로 추가되었습니다! (카테고리: {category})")

def show_list(target_list=None, header="전체 프롬프트 목록"):
    items = target_list if target_list is not None else prompts
    print(f"\n[ 📋 {header} ]")
    print("-" * 52)
    
    if not items:
        print("  등록된 프롬프트가 없습니다.")
        print("-" * 52)
        return False

    for idx, item in enumerate(items, 1):
        print(format_prompt_row(idx, item))
        
    print("-" * 52)
    print(f"총 {len(items)}개의 프롬프트")
    return True

def view_by_category():
    print("\n[ 📁 카테고리별 조회 ]")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"  {idx}. {cat}")
        
    choice = input("👉 조회할 카테고리 번호: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(CATEGORIES)):
        print("❌ 올바른 카테고리 번호가 아닙니다.")
        return

    selected_cat = CATEGORIES[int(choice) - 1]
    filtered = [p for p in prompts if p["category"] == selected_cat]
    show_list(filtered, f"'{selected_cat}' 카테고리 목록")

def search_prompt():
    print("\n[ 🔍 키워드 검색 ]")
    keyword = input("👉 검색어 입력 (제목 또는 내용): ").strip().lower()
    if not keyword:
        print("❌ 검색어를 입력해주세요.")
        return

    results = [
        p for p in prompts 
        if keyword in p["title"].lower() or keyword in p["content"].lower()
    ]
    show_list(results, f"'{keyword}' 검색 결과")

def show_detail():
    has_items = show_list()
    if not has_items:
        return

    choice = input("\n👉 상세 조회할 프롬프트 번호 입력: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print("❌ 올바른 번호가 아닙니다.")
        return

    item = prompts[int(choice) - 1]
    item["views"] = item.get("views", 0) + 1
    save_data(silent=True)

    fav_str = "⭐ (등록됨)" if item.get("favorite") else "❌ (미등록)"
    char_count = len(item["content"])
    line_count = len(item["content"].splitlines())

    print("\n" + "═" * 52)
    print(f"📌 제목     : {item['title']}")
    print(f"🏷️ 카테고리 : {item['category']}")
    print(f"⭐ 즐겨찾기 : {fav_str}")
    print(f"👁️ 조회수   : {item['views']} 회")
    print(f"📅 등록일시 : {item.get('created_at', '정보 없음')}")
    print(f"📊 글자수   : 약 {char_count}자 ({line_count}줄)")
    print("─" * 52)
    print("📝 프롬프트 본문:")
    print(item["content"])
    print("═" * 52)

def toggle_favorite():
    has_items = show_list()
    if not has_items:
        return

    choice = input("\n👉 즐겨찾기 설정/해제할 번호 입력: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print("❌ 올바른 번호가 아닙니다.")
        return

    target = prompts[int(choice) - 1]
    target["favorite"] = not target.get("favorite", False)
    save_data(silent=True)
    
    status = "⭐ 즐겨찾기에 추가" if target["favorite"] else "❌ 즐겨찾기에서 해제"
    print(f"\n✅ '{target['title']}' 프롬프트가 {status} 되었습니다.")

def show_favorites():
    fav_list = [p for p in prompts if p.get("favorite")]
    show_list(fav_list, "⭐ 즐겨찾기 프롬프트 목록")

def show_top_views():
    top_list = sorted(prompts, key=lambda x: x.get("views", 0), reverse=True)
    show_list(top_list, "🔥 인기 프롬프트 (조회수 순)")

def manage_prompt():
    has_items = show_list()
    if not has_items:
        return

    print("\n1) 프롬프트 수정  |  2) 프롬프트 삭제")
    sub_choice = input("👉 작업 선택: ").strip()

    if sub_choice not in ["1", "2"]:
        print("❌ 올바른 선택이 아닙니다.")
        return

    choice = input("👉 대상 프롬프트 번호 입력: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print("❌ 올바른 번호가 아닙니다.")
        return

    idx = int(choice) - 1
    target = prompts[idx]

    if sub_choice == "1":
        print(f"\n[ 수정 대상: {target['title']} ]")
        new_title = input(f"새 제목 (엔터 시 유지: {target['title']}): ").strip()
        new_content = input(f"새 내용 (엔터 시 유지): ").strip()

        if new_title:
            target["title"] = new_title
        if new_content:
            target["content"] = new_content

        save_data(silent=True)
        print("✅ 성공적으로 수정되었습니다.")

    elif sub_choice == "2":
        confirm = input(f"⚠️ 정말 '{target['title']}' 프롬프트를 삭제하시겠습니까? (y/N): ").strip().lower()
        if confirm == 'y':
            removed = prompts.pop(idx)
            save_data(silent=True)
            print(f"🗑️ '{removed['title']}' 프롬프트가 삭제되었습니다.")
        else:
            print("삭제가 취소되었습니다.")

def export_to_markdown():
    md = "# 📝 AI 프롬프트 라이브러리 컬렉션\n\n"
    md += f"> **생성 일시:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md += f"> **총 프롬프트 수:** {len(prompts)}개\n\n"
    
    md += "## 📊 카테고리 요약\n\n"
    grouped = {}
    for p in prompts:
        cat = p["category"]
        grouped.setdefault(cat, []).append(p)

    for cat, items in grouped.items():
        md += f"- **{cat}:** {len(items)}개\n"
    md += "\n---\n\n"

    for cat, items in grouped.items():
        md += f"## 📁 카테고리: {cat}\n\n"
        for p in items:
            fav = "⭐ " if p.get("favorite") else ""
            md += f"### {fav}{p['title']}\n"
            md += f"- **조회수:** {p.get('views', 0)}회\n"
            md += f"- **등록일:** {p.get('created_at', 'N/A')}\n\n"
            md += "```text\n"
            md += f"{p['content']}\n"
            md += "```\n\n"

    try:
        with open(MD_FILENAME, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"\n📄 [성공] '{MD_FILENAME}' 파일로 내보내기가 완료되었습니다!")
    except Exception as e:
        print(f"❌ [오류] 마크다운 내보내기 실패: {e}")

def main():
    load_data()
    
    while True:
        show_menu()
        choice = input("👉 메뉴 번호를 선택하세요: ").strip()

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
            show_top_views()
        elif choice == "9":
            manage_prompt()
        elif choice == "10":
            export_to_markdown()
        elif choice == "0":
            save_data(silent=True)
            print("\n👋 이용해주셔서 감사합니다. 프로그램을 안전하게 종료합니다!")
            break
        else:
            print("\n❌ 잘못된 입력입니다. 0부터 10 사이의 숫자를 입력해주세요.")

if __name__ == "__main__":
    main()
