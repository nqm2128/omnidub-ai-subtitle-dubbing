#!/usr/bin/env python3
"""Đổi tên file voice_clones theo ngôn ngữ của giọng. Dùng: python3 scripts/rename_voices.py [--apply]"""
import os, re, subprocess, sys, unicodedata
from collections import defaultdict

ROOT = "voice_clones"
APPLY = "--apply" in sys.argv
AUDIO = {".wav", ".mp3", ".flac", ".ogg"}
EXTS = AUDIO | {".txt"}

# Giới tính suy từ tên (mô tả gốc không nói rõ) -> nên nghe lại
CHECK = {("ja", "Satomi"), ("ja", "Otani"), ("zh", "Chen Mandarin Chinese"),
         ("zh", "Yu"), ("en", "Hope"), ("sk", "Jolana")}

# (mô tả gốc = phần trước dấu "_" đầu tiên, tên mới, giới tính). Thư mục "" = tiếng Việt.
VOICES = {
"": [
 ("Thanh Phong - Vietnamese, Ho Chi Minh Accent, Good for Narration", "Thanh Phong - Giọng Sài Gòn, hợp thuyết minh", "M"),
 ("Kim Tuyến - Middle-aged woman from Hanoi", "Kim Tuyến - Phụ nữ trung niên Hà Nội", "F"),
 ("Giang - Podcast", "Giang - Podcast", "F"),
 ("Ngan - Cute, Bubbly and Authentic", "Ngan - Dễ thương, tươi vui và chân thật", "F"),
 ("Bao Ngoc - A gentle Southern Vietnamese female voice, suitable for review, storytelling, and travel videos", "Bao Ngoc - Giọng nữ miền Nam dịu dàng, hợp review, kể chuyện và video du lịch", "F"),
 ("Announcer Van Phuc - Slow Narrator voice from the Voice of Vietnam", "Announcer Van Phuc - Giọng dẫn chậm rãi của Đài Tiếng nói Việt Nam", "M"),
 ("TVC Nhật Nam - Middle aged commercial voice actor from Hanoi", "TVC Nhật Nam - Diễn viên lồng tiếng quảng cáo trung niên Hà Nội", "M"),
 ("Dũng Trần - Smooth & Pacing Storyteller", "Dũng Trần - Người kể chuyện mượt mà, nhịp nhàng", "M"),
 ("Thuy Tien - Vietnamese Narrator", "Thuy Tien - Người dẫn truyện tiếng Việt", "F"),
 ("Minh Trí - Authentic Southern Vietnamese", "Minh Trí - Giọng miền Nam chuẩn", "M"),
 ("Sơn Hà - Vietnam Television, A professional Vietnamese broadcaster", "Sơn Hà - Phát thanh viên truyền hình chuyên nghiệp", "M"),
 ("Nhung - Clear, Formal and Professional", "Nhung - Rõ ràng, trang trọng và chuyên nghiệp", "F"),
 ("Bé Hồng Ân - Casual, informal tone.", "Bé Hồng Ân - Giọng thân mật, tự nhiên", "F"),
 ("Ca Dao - Literary writer from Huế", "Ca Dao - Nhà văn xứ Huế", "F"),
 ("Tram - Friendly Southern Vietnamese", "Tram - Thân thiện, giọng miền Nam", "F"),
 ("Thắm - Giọng Nữ Miền Bắc", "Thắm - Giọng Nữ Miền Bắc", "F"),
 ("Cam Hong - HCM Local", "Cam Hong - Người Sài Gòn", "F"),
 ("Giang Xì Gòn - Warm, Confident & Inspiring (11Labs)", "Giang Xì Gòn - Ấm áp, tự tin và truyền cảm hứng (11Labs)", "M"),
 ("Tuan Anh - Deep & Powerful Vietnamese", "Tuan Anh - Trầm và mạnh mẽ", "M"),
 ("Trong Nguyen - Natural, Deep, Clear", "Trong Nguyen - Tự nhiên, trầm, rõ ràng", "M"),
 ("Anh (11Labs)", "Anh (11Labs)", "F"),
 ("Tung Dang - Deep, Warm and Resonant", "Tung Dang - Trầm, ấm và vang", "M"),
 ("Diễm Tuyết - Crisp, Formal & Professional (11Labs)", "Diễm Tuyết - Rõ nét, trang trọng và chuyên nghiệp (11Labs)", "F"),
 ("Actor Pham Hung - Old Male with Saigon accent", "Actor Pham Hung - Nam lớn tuổi giọng Sài Gòn", "M"),
 ("Hien (11Labs)", "Hien (11Labs)", "F"),
 ("Tony Hoang", "Tony Hoang", "M"),
 ("Huyen (11Labs)", "Huyen (11Labs)", "F"),
 ("Trang - Soft, Whispery and Peaceful", "Trang - Mềm mại, thì thầm và bình yên", "F"),
 ("MC Duy Minh - Vietnamese MC from Sài Gòn. Good for announcers, narration, advertising, and TV (11Labs)", "MC Duy Minh - MC Sài Gòn, hợp thông báo, thuyết minh, quảng cáo và truyền hình (11Labs)", "M"),
 ("Hạnh - Smooth, Clear & Feminine (11Labs)", "Hạnh - Mượt mà, rõ ràng và nữ tính (11Labs)", "F"),
 ("Trieu Duong - Deep, Calm and Resonant", "Trieu Duong - Trầm, điềm tĩnh và vang", "M"),
 ("Nhu (11Labs)", "Nhu (11Labs)", "F"),
 ("Phanh - Storytelling (11Labs)", "Phanh - Kể chuyện (11Labs)", "M"),
 ("Quang Nguyen (11Labs)", "Quang Nguyen (11Labs)", "M"),
 ("Ninh Đôn (11Labs)", "Ninh Đôn (11Labs)", "M"),
 ("Nhật Phong (11Labs)", "Nhật Phong (11Labs)", "M"),
 ("Thanh Đọc Sách - Clear, Steady & Informative (11Labs)", "Thanh Đọc Sách - Rõ ràng, ổn định và giàu thông tin (11Labs)", "M"),
 ("Thảo (11Labs)", "Thảo (11Labs)", "F"),
 ("Thức Dovin - Deep & Warm Audiobook (VN), Premium high-quality Vietnamese male voice", "Thức Dovin - Sách nói trầm ấm, giọng nam tiếng Việt chất lượng cao", "M"),
 ("Thắm (11Labs)", "Thắm (11Labs)", "F"),
 ("Mai (11Labs)", "Mai (11Labs)", "F"),
 ("Trang (11Labs)", "Trang (11Labs)", "F"),
 ("Trieu Duong (11Labs)", "Trieu Duong (11Labs)", "M"),
 ("Trung (11Labs)", "Trung (11Labs)", "M"),
 ("Kenh (11Labs)", "Kenh (11Labs)", "M"),
 ("Ngân Nguyễn (11Labs)", "Ngân Nguyễn (11Labs)", "F"),
 ("Trung Caha (11Labs)", "Trung Caha (11Labs)", "M"),
 ("Tuan Anh - StoryTeller, Warm & Deep (11Labs)", "Tuan Anh - Người kể chuyện, ấm và trầm (11Labs)", "M"),
 ("Tung Dang (11Labs)", "Tung Dang (11Labs)", "M"),
 ("Đức (11Labs)", "Đức (11Labs)", "M"),
],
"en": [
 ("Michael C. Vincent - Confident, Expressive", "Michael C. Vincent - Confident, Expressive", "M"),
 ("Christopher - Gentle and Trustworthy", "Christopher - Gentle and Trustworthy", "M"),
 ("Adam Stone - Smooth, Deep and Relaxed", "Adam Stone - Smooth, Deep and Relaxed", "M"),
 ("James - Husky, Engaging and Bold", "James - Husky, Engaging and Bold", "M"),
 ("Hope - upbeat and clear", "Hope - Upbeat and Clear", "F"),
 ("Mark - Natural Conversations", "Mark - Natural Conversations", "M"),
 ("Adam - American, Dark and Tough", "Adam - American, Dark and Tough", "M"),
 ("Peter", "Peter - Confident and Credible", "M"),
 ("Adam", "Adam - Rich Radio Announcer", "M"),
 ("Spuds Oxley - Grandpa", "Spuds Oxley - Grandpa", "M"),
],
"tr": [
 ("Derya - Dynamic and Friendly Narrator", "Derya - Dinamik ve Samimi Anlatıcı", "F"),
 ("Doga - Upbeat and Rich", "Doga - Neşeli ve Zengin Ses", "M"),
 ("Doga - Audiobook Master", "Doga - Sesli Kitap Ustası", "M"),
 ("Belma - Dynamic and Clear Narrator", "Belma - Dinamik ve Net Anlatıcı", "F"),
 ("Cavit Pancar - Epic Powerful Historical", "Cavit Pancar - Destansı, Güçlü Tarihî Anlatım", "M"),
 ("Adam - Calm, Relaxing and Informative", "Adam - Sakin, Rahatlatıcı ve Bilgilendirici", "M"),
 ("Adam - Deep, Professional and Serious", "Adam - Derin, Profesyonel ve Ciddi", "M"),
 ("Mark - Cartoonish, Funny and Cheerful", "Mark - Karikatür Tarzı, Komik ve Neşeli", "M"),
 ("Eda Atlas - Smooth, Clear and Balanced", "Eda Atlas - Akıcı, Net ve Dengeli", "F"),
 ("Fatih Yıldırım - Deep, Clear and Rich", "Fatih Yıldırım - Derin, Net ve Zengin", "M"),
],
"pt": [
 ("Roberta - Smooth and Confident", "Roberta - Suave e Confiante", "F"),
 ("Will - Deep, Smooth and Affectionate", "Will - Grave, Suave e Afetuoso", "M"),
 ("Paulo - Expressive and Confident", "Paulo - Expressivo e Confiante", "M"),
 ("Adriano - Deep, Gravelly and Rugged", "Adriano - Grave, Rouco e Rústico", "M"),
 ("Keren - Sweet, Vibrant and Rhythmic", "Keren - Doce, Vibrante e Ritmada", "F"),
 ("Lax - Funny, Sarcastic and Smooth", "Lax - Engraçado, Sarcástico e Suave", "M"),
 ("Matheus - Friendly and Energetic", "Matheus - Amigável e Enérgico", "M"),
 ("Victor Power - Wise, Dramatic and Deep", "Victor Power - Sábio, Dramático e Grave", "M"),
 ("Otto - Intimidating and Aggressive", "Otto - Intimidador e Agressivo", "M"),
 ("Yasmin Alves - Light, Clear and Musical", "Yasmin Alves - Leve, Clara e Musical", "F"),
],
"sk": [
 ("Luki Zajo - Lively, Deep and Focused", "Luki Zajo - Živý, hlboký a sústredený", "M"),
 ("Tibor", "Tibor - Zrelý, pokojný a hlboký", "M"),
 ("Andrej - Balanced and Airy", "Andrej - Vyvážený a ľahký", "M"),
 ("Julia - Young & Airy", "Julia - Mladá a ľahká", "F"),
 ("Ingrid - Steady Storyteller", "Ingrid - Vyrovnaná rozprávačka", "F"),
 ("Jolana", "Jolana - Pokojná a príjemná", "F"),
 ("Adam - Young and Energetic", "Adam - Mladý a energický", "M"),
 ("Peter - Alien, Friendly and Soft", "Peter - Mimozemský, priateľský a jemný", "M"),
 ("Jaro", "Jaro - Neutrálny slovenský hlas", "M"),
 ("Alex - Pleasant, Warm and Trustworthy", "Alex - Príjemný, srdečný a dôveryhodný", "M"),
],
"fr": [
 ("Jeunot - Professional, Clear and Positve", "Jeunot - Professionnel, clair et positif", "M"),
 ("Audrey - Energetic Commercial", "Audrey - Publicitaire dynamique", "F"),
 ("Nicolas - Narrator", "Nicolas - Narrateur", "M"),
 ("François Louis - Deep, Warm and Poised", "François Louis - Grave, chaleureux et posé", "M"),
 ("Victor - Casual and Conversational", "Victor - Décontracté et conversationnel", "M"),
 ("Martin Dupont - Deep, Warm and Aged", "Martin Dupont - Grave, chaleureux et mûr", "M"),
 ("Guillaume - Narrator", "Guillaume - Narrateur", "M"),
 ("Adam - warm and friendly", "Adam - Chaleureux, amical, québécois", "M"),
 ("Adrien - Deep, Comforting and Warm", "Adrien - Grave, réconfortant et chaleureux", "M"),
 ("Yann - Narrator", "Yann - Narrateur", "M"),
],
"ja": [
 ("Satomi - Calm, Smooth and Clear", "Satomi - 穏やかで滑らかで明瞭", "F"),
 ("Kenzo - Calm, Soft and Measured", "Kenzo - 穏やかで柔らかく落ち着いた声", "M"),
 ("Shizuka - Natural and Soft", "Shizuka - 自然で柔らかい", "F"),
 ("Ishibashi - Inviting, Natural and Smoky", "Ishibashi - 魅力的で自然、スモーキー", "M"),
 ("Kuon - Cheerful, Clear and Steady", "Kuon - 明るく明瞭で安定", "F"),
 ("Yui - Warm, Clear and Natural", "Yui - 温かく明瞭で自然", "F"),
 ("Mitsuki - inviting, Steady and Clear", "Mitsuki - 親しみやすく安定して明瞭", "F"),
 ("Kozy - Inviting, Measured and Guttural", "Kozy - 親しみやすく落ち着いた喉声", "M"),
 ("Hiroki - Calm and Precise", "Hiroki - 穏やかで正確", "M"),
 ("Otani - Inviting, Clear and Measured", "Otani - 親しみやすく明瞭で落ち着いた声", "M"),
 ("Hinata - Inviting, Smooth and Measured", "Hinata - 親しみやすく滑らかで落ち着いた声", "M"),
 ("Hina - cute and friendly", "Hina - かわいくて親しみやすい", "F"),
],
"es": [
 ("Dan - Upbeat, Dynamic and Friendly", "Dan - Animado, dinámico y amistoso", "M"),
 ("David Martin - Confident and Balanced", "David Martin - Seguro y equilibrado", "M"),
 ("Alberto Rodríguez - Serious, Narrative", "Alberto Rodríguez - Serio y narrativo", "M"),
 ("Enrique M. Nieto - Credible and Rich", "Enrique M. Nieto - Creíble y rico", "M"),
 ("Miguel - Deep, Rich and Cinematic", "Miguel - Profundo, rico y cinematográfico", "M"),
 ("Sara Martin - Gentle and Layered", "Sara Martin - Suave y matizada", "F"),
 ("Martin Osborne - Intimate and Warm", "Martin Osborne - Íntimo y cálido", "M"),
 ("Rada - Relaxed, Confident, Calm", "Rada - Relajado, seguro y tranquilo", "M"),
 ("Fernando Martínez - Rapid, Persuasive", "Fernando Martínez - Rápido y persuasivo", "M"),
 ("Carmelo - Mature, Mysterious and Clear", "Carmelo - Maduro, misterioso y claro", "M"),
],
"cs": [
 ("Oliver - Smooth and Engaging", "Oliver - Jemný a poutavý", "M"),
 ("Jan - Kind Educator", "Jan - Laskavý pedagog", "M"),
 ("Lukas - Calm, Neutral and Educational", "Lukas - Klidný, neutrální a vzdělávací", "M"),
 ("Zazy - Clear Audiobook Narrator", "Zazy - Čistý vypravěč audioknih", "M"),
 ("Adam - Velvety and Conversational", "Adam - Sametový a konverzační", "M"),
 ("Zdeněk - Strong and Deep", "Zdeněk - Silný a hluboký", "M"),
 ("Daniel - Pleasant Receptionist", "Daniel - Příjemný recepční", "M"),
 ("Mirek - Slow and Flowy Storyteller", "Mirek - Pomalý a plynulý vypravěč", "M"),
 ("Anet - Youthful and Lively", "Anet - Mladistvá a živá", "F"),
 ("Pawel - Cinematic, Deep and Confident", "Pawel - Filmový, hluboký a sebevědomý", "M"),
],
"ru": [
 ("Prince Nur - Smooth, Rich and Engaging", "Prince Nur - Мягкий, насыщенный и притягательный", "M"),
 ("Nikolay - Confident, Clear and Engaging", "Nikolay - Уверенный, чёткий и увлекательный", "M"),
 ("Alex Bell - Deep and Confident", "Alex Bell - Глубокий и уверенный", "M"),
 ("Artem Lebedev - Captivating and Engaging", "Artem Lebedev - Завораживающий и увлекательный", "M"),
 ("Dmitry - Energetic and Confident", "Dmitry - Энергичный и уверенный", "M"),
 ("Alexandr Vlasov - Vibrant and Energetic", "Alexandr Vlasov - Яркий и энергичный", "M"),
 ("Marina - Soft, Clear and Warm", "Marina - Мягкая, чёткая и тёплая", "F"),
 ("Denis - Pleasant, Engaging and Friendly", "Denis - Приятный, увлекательный и дружелюбный", "M"),
 ("Prince Nur - Deep, Rich and Balanced", "Prince Nur - Глубокий, насыщенный и сбалансированный", "M"),
 ("Stanislav - Deep, Empathetic and Warm", "Stanislav - Глубокий, чуткий и тёплый", "M"),
],
"zh": [  # giọng Đài Loan dùng phồn thể, còn lại giản thể
 ("Jason Chen - Deep, Magnetic and Calm", "Jason Chen - 低沉、磁性、沉稳", "M"),
 ("Haoran - Deep, Calm and Steady", "Haoran - 低沉、沉稳且平稳", "M"),
 ("Anna Su - Trustworthy, Clear and Natural", "Anna Su - 可信、清晰且自然", "F"),
 ("Evan - Warm, Soothing and Soft", "Evan - 溫暖、舒緩且柔和", "M"),
 ("Amy - Friendly, Young and Natural", "Amy - 友善、年轻且自然", "F"),
 ("Chen Mandarin Chinese", "Chen - 帶輕柔台灣口音的標準華語", "M"),
 ("Evan Zhao - Warm, Calm and Trustworthy", "Evan Zhao - 温暖、沉稳且值得信赖", "M"),
 ("Shan Shan - Young Energetic Female", "Shan Shan - 年轻活力的女声", "F"),
 ("Lee Ting Ting - Young, Gentle and Sweet", "Lee Ting Ting - 年輕、溫柔且甜美", "F"),
 ("Anna Su - Casual, Friendly and Bright", "Anna Su - 隨和、友善且明亮", "F"),
 ("Stacy - Young, Sweet and Cute", "Stacy - 年輕、甜美且可愛", "F"),
 ("Mingyao Ye - Sad and Broken Hearted", "Mingyao Ye - 悲伤而心碎", "F"),
 ("Neil Chuang - Deep, Trustworthy and Rich", "Neil Chuang - 低沉、可靠且醇厚", "M"),
 ("Kevin Tu - Natural, Steady and Calm", "Kevin Tu - 自然、平穩且沉著", "M"),
 ("Martin Li - Raspy, Serious and Deep", "Martin Li - 沙哑、严肃且低沉", "M"),
 ("Yui - Delicate, Graceful and Soothing", "Yui - 細膩、優雅且舒緩", "F"),
 ("James Gao - Calm, Friendly and Warm", "James Gao - 沉稳、友善且温暖", "M"),
 ("Yu - Youthful, Energetic and Engaging", "Yu - 青春、活力且引人入勝", "M"),
 ("Tiffy - Taiwanese Bilingual Narrator", "Tiffy - 台灣雙語旁白", "F"),
],
"ko": [
 ("Anna Kim - Tender, Calm and Clear", "Anna Kim - 부드럽고 차분하며 또렷한", "F"),
 ("Dohyeon - Whisper, Measured and Neutral", "Dohyeon - 속삭이듯 절제되고 중립적인", "M"),
 ("Taehyung - Natural, Friendly and Clear", "Taehyung - 자연스럽고 친근하며 또렷한", "M"),
 ("Krys - Cheerful, Clear and Measured", "Krys - 밝고 또렷하며 안정적인", "M"),
 ("Hyunbin - Diplomatic, Clear and Measured", "Hyunbin - 외교적이고 또렷하며 절제된", "M"),
 ("Hyuk - Encourging and Clear", "Hyuk - 격려하듯 또렷한", "M"),
 ("Bin - Measured and Serious", "Bin - 절제되고 진지한", "M"),
 ("Seulki - Inviting, Calm and Measured", "Seulki - 포근하고 차분하며 안정적인", "F"),
 ("Chris - Warm and Clear", "Chris - 따뜻하고 또렷한", "M"),
 ("Chungman - Meditative, Clear and Soft", "Chungman - 명상적이고 또렷하며 부드러운", "F"),
],
"de": [
 ("Mila - Confident and Opinionated", "Mila - Selbstbewusst und meinungsstark", "F"),
 ("Leon Stern - Rich and Deep", "Leon Stern - Voll und tief", "M"),
 ("Otto - Casual and Normal", "Otto - Locker und natürlich", "M"),
 ("Alexander - Deep TV Narrator", "Alexander - Tiefer TV-Sprecher", "M"),
 ("Thomas Schendel - Authoritative and Calm", "Thomas Schendel - Autoritär und ruhig", "M"),
 ("Helmut Stieglbauer - Deep and Dynamic", "Helmut Stieglbauer - Tief und dynamisch", "M"),
 ("Helmut - German Epic Trailer Voice", "Helmut - Epische Trailer-Stimme", "M"),
 ("Christian - Warm and Captivating", "Christian - Warm und fesselnd", "M"),
 ("Niander Wallace", "Niander Wallace - Reife, tiefe Stimme", "M"),
 ("Tristan Medersburg - Trustworthy", "Tristan Medersburg - Vertrauenswürdig", "M"),
],
}

def norm(s):
    s = unicodedata.normalize("NFC", s).replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip(" .").casefold()

def clean(s):
    return re.sub(r'[\\/:*?"<>|]', "", s).strip()

def lookup(table, stem):
    head = norm(stem.split("_")[0])
    if head in table:
        return head, table[head]
    # tên gốc bị cắt cụt: chỉ chấp nhận khi đủ dài và khớp duy nhất
    c = [k for k in table if len(head) >= 20 and k.startswith(head)]
    return (c[0], table[c[0]]) if len(c) == 1 else (None, None)

plan, problems, warns = [], [], []
for lang, rows in VOICES.items():
    folder = os.path.join(ROOT, lang)
    if not os.path.isdir(folder):
        problems.append(f"Thiếu thư mục {folder}")
        continue
    table = {norm(o): (clean(n), g, o) for o, n, g in rows}
    new_stems = {f"{n}_{g}" for n, g, _ in table.values()}
    groups, used, seen = defaultdict(set), set(), {}
    for fn in os.listdir(folder):
        stem, ext = os.path.splitext(fn)
        if ext.lower() in EXTS:
            groups[stem].add(ext)
    olds = {s + e for s, es in groups.items() for e in es}
    for stem, exts in sorted(groups.items()):
        if stem in new_stems:
            continue  # đã đổi từ lần chạy trước
        key, hit = lookup(table, stem)
        if not hit:
            problems.append(f"Không khớp bảng dịch: {folder}/{stem}")
            continue
        used.add(key)
        new_head, g, old_head = hit
        new_stem = f"{new_head}_{g}"
        if new_stem in seen:
            problems.append(f"Trùng tên mới '{new_stem}': {stem} và {seen[new_stem]}")
            continue
        seen[new_stem] = stem
        if len((new_stem + ".flac").encode("utf-8")) > 200:
            problems.append(f"Tên mới quá dài: {new_stem}")
        if not exts & AUDIO:
            problems.append(f"Chỉ có .txt, thiếu audio: {folder}/{stem}")
        if ".txt" not in exts:
            warns.append(f"Thiếu transcript .txt: {folder}/{stem}")
        if (lang, old_head.split(" - ")[0].strip()) in CHECK:
            warns.append(f"Giới tính suy từ tên, nên nghe lại: [{lang or 'vi'}] {new_stem}")
        for ext in sorted(exts):
            new = new_stem + ext
            if os.path.exists(os.path.join(folder, new)) and new not in olds:
                problems.append(f"Tên mới đã tồn tại: {folder}/{new}")
            plan.append((folder, stem + ext, new))
    for k, (_, _, o) in table.items():
        if k not in used and f"{table[k][0]}_{table[k][1]}" not in {s for s in groups}:
            warns.append(f"Có trong bảng nhưng không thấy file: [{lang or 'vi'}] {o}")

out = ["| Thư mục | Tên cũ | Tên mới |", "|---|---|---|"]
out += [f"| {f} | {o} | {n} |" for f, o, n in plan]
out += ["", f"Tổng số file sẽ đổi: {len(plan)}"]
out += [f"⚠️ {w}" for w in warns] + [f"❌ {p}" for p in problems]
text = "\n".join(out)
print(text)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "w", encoding="utf-8") as fh:
        fh.write(text)

if problems:
    print("\nCó lỗi, KHÔNG đổi tên gì cả. Sửa bảng VOICES rồi chạy lại.")
    sys.exit(1)
if APPLY:
    for folder, old, new in plan:
        subprocess.run(["git", "mv", os.path.join(folder, old), os.path.join(folder, new)], check=True)
    print("Đã đổi tên xong.")
else:
    print("\nChế độ xem trước, chưa đổi gì. Chạy lại với apply để đổi thật.")
