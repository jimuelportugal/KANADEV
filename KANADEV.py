# KANADEV — a lightweight kana learning game built with pygame
# ------------------------------------------------------------
# Modes:
#   1) Flashcards — browse kana with romaji
#   2) Quiz — multiple choice (pick the correct romaji)
#   3) Type — type the romaji for the shown kana
#
# Features:
#   • Simple spaced practice: items you miss appear more often
#   • Tracks accuracy/streaks, session score, and saves per-kana mastery
#   • Works with Hiragana and Katakana (toggle in menu)
#   • All in one file; no assets required
#
# How to run (Windows):
#   py -m pip install pygame
#   py kanadev.py
#
# Keys:
#   • ESC: go back / open menu
#   • Enter: confirm
#   • In Type mode: type romaji then Enter
#   • In Flashcards: SPACE to flip, Left/Right to navigate
#
# Tip: The progress file 'kanadev_progress.json' is created next to the script.


# pyinstaller --onedir --noconsole KANADEV.py
# pyinstaller --onefile --noconsole --noupx KANADEV.py

import json
import math
import os
import random
import sys
from typing import Dict, List, Tuple

import pygame


HIRAGANA = {
    # a-row
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    # k-row
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    # s-row
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    # t-row
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    # n-row
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    # h-row
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    # m-row
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    # y-row
    "や": "ya", "ゆ": "yu", "よ": "yo",
    # r-row
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    # w-row + n
    "わ": "wa", "を": "wo", "ん": "n",
    # dakuten/handakuten (basic)
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    # youon (contracted)
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja",  "じゅ": "ju",  "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
}

KATAKANA = {
    # a-row
    "ア": "a", "イ": "i", "ウ": "u", "エ": "e", "オ": "o",
    # k-row
    "カ": "ka", "キ": "ki", "ク": "ku", "ケ": "ke", "コ": "ko",
    # s-row
    "サ": "sa", "シ": "shi", "ス": "su", "セ": "se", "ソ": "so",
    # t-row
    "タ": "ta", "チ": "chi", "ツ": "tsu", "テ": "te", "ト": "to",
    # n-row
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no",
    # h-row
    "ハ": "ha", "ヒ": "hi", "フ": "fu", "ヘ": "he", "ホ": "ho",
    # m-row
    "マ": "ma", "ミ": "mi", "ム": "mu", "メ": "me", "モ": "mo",
    # y-row
    "ヤ": "ya", "ユ": "yu", "ヨ": "yo",
    # r-row
    "ラ": "ra", "リ": "ri", "ル": "ru", "レ": "re", "ロ": "ro",
    # w-row + n
    "ワ": "wa", "ヲ": "wo", "ン": "n",
    # dakuten/handakuten
    "ガ": "ga", "ギ": "gi", "グ": "gu", "ゲ": "ge", "ゴ": "go",
    "ザ": "za", "ジ": "ji", "ズ": "zu", "ゼ": "ze", "ゾ": "zo",
    "ダ": "da", "ヂ": "ji", "ヅ": "zu", "デ": "de", "ド": "do",
    "バ": "ba", "ビ": "bi", "ブ": "bu", "ベ": "be", "ボ": "bo",
    "パ": "pa", "ピ": "pi", "プ": "pu", "ペ": "pe", "ポ": "po",
    # youon
    "キャ": "kya", "キュ": "kyu", "キョ": "kyo",
    "シャ": "sha", "シュ": "shu", "ショ": "sho",
    "チャ": "cha", "チュ": "chu", "チョ": "cho",
    "ニャ": "nya", "ニュ": "nyu", "ニョ": "nyo",
    "ヒャ": "hya", "ヒュ": "hyu", "ヒョ": "hyo",
    "ミャ": "mya", "ミュ": "myu", "ミョ": "myo",
    "リャ": "rya", "リュ": "ryu", "リョ": "ryo",
    "ギャ": "gya", "ギュ": "gyu", "ギョ": "gyo",
    "ジャ": "ja",  "ジュ": "ju",  "ジョ": "jo",
    "ビャ": "bya", "ビュ": "byu", "ビョ": "byo",
    "ピャ": "pya", "ピュ": "pyu", "ピョ": "pyo",
}

# -----------------------------
# Utility / persistence
# -----------------------------
SAVE_FILE = "kanadev_progress.json"
WORDS_FILE = "words.json"

def load_progress() -> Dict[str, Dict]:
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for script in ("hiragana", "katakana"):
                    data.setdefault(script, {})
                # Convert any float mastery to int (for backward compatibility)
                for script in ("hiragana", "katakana"):
                    for k, v in data[script].items():
                        data[script][k] = max(1, min(10, int(round(float(v) * 10)) if isinstance(v, float) and v <= 1 else int(v)))
                # Add best_score if missing
                if "best_score" not in data:
                    data["best_score"] = {"hiragana": 0, "katakana": 0}
                for script in ("hiragana", "katakana"):
                    data["best_score"].setdefault(script, 0)
                return data
        except Exception:
            pass
    return {"hiragana": {}, "katakana": {}, "best_score": {"hiragana": 0, "katakana": 0}}

def save_progress(progress: Dict[str, Dict]):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def choice_weight(mastery: int) -> float:
    # Lower mastery (1) = higher weight, higher mastery (5) = lower weight
    return (6 - mastery) ** 2 + 0.01


# -----------------------------
# UI primitives
# -----------------------------
pygame.init()

WIDTH, HEIGHT = 900, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KANADEV")

CLOCK = pygame.time.Clock()
FPS = 60

FONT_LG = pygame.font.SysFont("Noto Sans CJK JP, Meiryo, Yu Gothic, Arial Unicode MS, Arial", 160, bold=True)
FONT_MD = pygame.font.SysFont("Segoe UI, Arial", 36)
FONT_SM = pygame.font.SysFont("Segoe UI, Arial", 24)

BG = (29, 35, 45)
PANEL = (42, 51, 66)
ACCENT = (98, 190, 255)
OK = (90, 207, 140)
WARN = (255, 120, 120)
MUTED = (170, 180, 190)
WHITE = (240, 244, 248)


def draw_text(surface, text, font, color, center=None, topleft=None, align="center"):
    text = text.upper()  # Force uppercase
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = center
    elif topleft:
        rect.topleft = topleft
    # Remove the old align logic that forced centering for topleft!
    surface.blit(img, rect)
    return rect


class Button:
    def __init__(self, rect, label, on_click, *, key_hint=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.key_hint = key_hint
        self.hover = False

    def draw(self, surf):
        color = tuple(min(255, c + (18 if self.hover else 0)) for c in PANEL)
        pygame.draw.rect(surf, color, self.rect, border_radius=12)
        pygame.draw.rect(surf, (60, 72, 90), self.rect, width=2, border_radius=12)
        draw_text(surf, self.label, FONT_MD, WHITE, center=self.rect.center, align="center")

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


class InputLine:
    def __init__(self):
        self.text = ""
        self.cursor = True
        self.timer = 0

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return "submit"
            else:
                ch = event.unicode
                if ch.isprintable():
                    self.text += ch
        return None

    def draw(self, surf, rect):
        pygame.draw.rect(surf, PANEL, rect, border_radius=12)
        pygame.draw.rect(surf, (60, 72, 90), rect, 2, border_radius=12)
        self.timer += 1
        if self.timer % 30 == 0:
            self.cursor = not self.cursor
        shown = self.text.upper() + ("|" if self.cursor else " ")
        # Center the text in the input box
        img = FONT_MD.render(shown, True, WHITE)
        img_rect = img.get_rect(center=rect.center)
        surf.blit(img, img_rect)

# -----------------------------
# Scenes
# -----------------------------
class Scene:
    def handle(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surf):
        pass


class Menu(Scene):
    def __init__(self, app):
        self.app = app
        gap = 16
        w, h = 240, 56
        start_x = WIDTH // 2 - w // 2
        start_y = HEIGHT // 2 - (3 * (h + gap)) // 2

        # Main menu buttons
        self.buttons: List[Button] = [
            Button((start_x, start_y + 0*(h+gap), w, h), "Flashcards", lambda: app.change_scene(Flashcards(app))),
            Button((start_x, start_y + 1*(h+gap), w, h), "Quiz", lambda: app.change_scene(Quiz(app))),
            Button((start_x, start_y + 2*(h+gap), w, h), "Type", lambda: app.change_scene(TypeMode(app))),
        ]

        # Switch script label (bottom left)
        self.switch_label_rect = None
        self.switch_label = app.script_name.capitalize()

    def handle(self, event):
        for b in self.buttons:
            b.handle(event)
        # Handle click on switch label
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.switch_label_rect and self.switch_label_rect.collidepoint(event.pos):
                self.app.toggle_script()
                self.switch_label = self.app.script_name.capitalize()

    def update(self, dt):
        pass

    def draw(self, surf):
        surf.fill(BG)
        draw_text(surf, "KANADEV", FONT_MD, ACCENT, center=(WIDTH//2, 120))
        for b in self.buttons:
            b.draw(surf)
        color = ACCENT if self.switch_label_rect and self.switch_label_rect.collidepoint(pygame.mouse.get_pos()) else WHITE
        self.switch_label_rect = draw_text(surf, self.switch_label, FONT_MD, color, topleft=(30, HEIGHT - 60))
        draw_text(surf, "ESC to quit", FONT_SM, MUTED, center=(WIDTH//2, HEIGHT-28))

class Scene:
    def _bump_mastery(self, kana, delta):
        prog = self.app.progress[self.app.script_name]
        cur = int(prog.get(kana, 1))
        cur = max(1, min(10, cur + delta))
        prog[kana] = cur    

class Quiz(Scene):
    def __init__(self, app):
        self.app = app
        self.score = 0
        self.streak = 0
        self.round = 0
        self.feedback = ""
        self.feedback_timer = 0
        self.choices: List[Tuple[str, str]] = []  # list of (kana, romaji)
        self.correct_idx = 0
        self.kana = None

        # --- Kana group selection ---
        self.selecting = True
        self.kana_groups = [
            ("BASIC", self._is_basic),
            ("DAKUTEN & HANDAKUTEN", self._is_daku),
            ("COMBO KANA", self._is_combo),
        ]
        self.selected_groups = [True, True, True]  # All selected by default

        # Build group selection "buttons" (just clickable text)
        self.group_rects = [None, None, None]
        self.start_btn_rect = None

        # build answer buttons
        self.buttons: List[Button] = []
        w, h, gap = 260, 56, 18
        start_x = WIDTH//2 - w//2
        start_y = HEIGHT//2 + 40
        for i in range(4):
            btn = Button((start_x, start_y + i*(h+gap), w, h), "", lambda i=i: self.choose(i))
            self.buttons.append(btn)

        self.pick_question()

    # --- Kana group filters ---
    def _is_basic(self, kana):
        return kana in (
            list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん") +
            list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
        )
    def _is_daku(self, kana):
        return kana in (
            list("がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ") +
            list("ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ")
        )
    def _is_combo(self, kana):
        return kana in (
            list("きゃきゅきょしゃしゅしょちゃちゅちょにゃにゅにょひゃひゅひょみゃみゅみょりゃりゅりょぎゃぎゅぎょじゃじゅじょびゃびゅびょぴゃぴゅぴょ") +
            list("キャキュキョシャシュショチャチュチョニャニュニョヒャヒュヒョミャミュミョリャリュリョギャギュギョジャジュジョビャビュビョピャピュピョ")
        )

    def _filtered_kana(self):
        filters = [f for sel, (_, f) in zip(self.selected_groups, self.kana_groups) if sel]
        if not filters:
            return []
        return [k for k in self.app.table.keys() if any(f(k) for f in filters)]

    def weighted_pick(self) -> str:
        prog = self.app.progress[self.app.script_name]
        kana_list = self._filtered_kana()
        if not kana_list:
            return random.choice(list(self.app.table.keys()))
        items = []
        for k in kana_list:
            m = int(prog.get(k, 1))
            items.append((k, choice_weight(m)))
        total = sum(w for _, w in items)
        r = random.random() * total
        acc = 0
        for k, w in items:
            acc += w
            if r <= acc:
                return k
        return items[-1][0]

    def pick_question(self):
        self.kana = self.weighted_pick()
        correct_romaji = self.app.table[self.kana]
        # sample 3 wrong answers
        all_romaji = list(set(self.app.table.values()))
        wrongs = [r for r in all_romaji if r != correct_romaji]
        random.shuffle(wrongs)
        opts = [correct_romaji] + wrongs[:3]
        random.shuffle(opts)
        self.correct_idx = opts.index(correct_romaji)
        self.choices = [(self.kana, r) for r in opts]
        for i, btn in enumerate(self.buttons):
            btn.label = opts[i].upper()

    def choose(self, idx):
        correct = idx == self.correct_idx
        script = self.app.script_name
        if correct:
            self.streak += 1
            self.score = self.streak
            # Update best score if needed
            if self.score > self.app.progress["best_score"][script]:
                self.app.progress["best_score"][script] = self.score
            self.feedback = "Correct"
            self._bump_mastery(self.kana, +1)
        else:
            self.streak = 0
            self.score = 0
            self.feedback = f"{self.app.table[self.kana]}"
            self._bump_mastery(self.kana, -1)
        self.feedback_timer = 45
        save_progress(self.app.progress)
        self.round += 1
        self.pick_question()

    def handle(self, event):
        if self.selecting:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for i, rect in enumerate(self.group_rects):
                    if rect and rect.collidepoint(pos):
                        self.selected_groups[i] = not self.selected_groups[i]
                if self.start_btn_rect and self.start_btn_rect.collidepoint(pos):
                    if any(self.selected_groups):
                        self.selecting = False
                        self.pick_question()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.change_scene(Menu(self.app))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.change_scene(Menu(self.app))
            for b in self.buttons:
                b.handle(event)

    def update(self, dt):
        if not self.selecting and self.feedback_timer > 0:
            self.feedback_timer -= 1

    def draw(self, surf):
        surf.fill(BG)
        if self.selecting:
            draw_text(surf, "Quiz", FONT_MD, ACCENT, center=(WIDTH//2, 120))
            y = 220
            self.group_rects = []
            for i, (label, _) in enumerate(self.kana_groups):
                checked = self.selected_groups[i]
                color = ACCENT if checked else MUTED
                # Center the group label horizontally
                rect = draw_text(surf, label, FONT_MD, color, center=(WIDTH//2, y), align="center")
                self.group_rects.append(rect)
                y += 70
            btn_color = OK if any(self.selected_groups) else MUTED
            self.start_btn_rect = draw_text(surf, "START", FONT_MD, btn_color, center=(WIDTH//2, int(HEIGHT * 0.8)))
            draw_text(surf, "ESC to cancel", FONT_SM, MUTED, center=(WIDTH//2, HEIGHT-28))
        else:
            draw_text(surf, "Quiz — choose the romaji", FONT_SM, MUTED, topleft=(24, 20))
            draw_text(surf, f"Score: {self.score}   Streak: {self.streak}", FONT_SM, MUTED, topleft=(24, 52))
            best = self.app.progress.get("best_score", {}).get(self.app.script_name, 0)
            draw_text(surf, f"Best: {best}", FONT_SM, WARN, topleft=(WIDTH - 180, 52))
            draw_text(surf, self.kana, FONT_LG, WHITE, center=(WIDTH//2, HEIGHT//2 - 80))
            for b in self.buttons:
                b.draw(surf)
            if self.feedback_timer > 0:
                color = OK if self.feedback.lower() == "correct" else WARN
                draw_text(surf, self.feedback, FONT_MD, color, center=(WIDTH//2, 100))


class Flashcards(Scene):
    def __init__(self, app):
        self.app = app
        # --- Kana group selection ---
        self.selecting = True
        self.kana_groups = [
            ("BASIC", self._is_basic),
            ("DAKUTEN & HANDAKUTEN", self._is_daku),
            ("COMBO KANA", self._is_combo),
        ]
        self.selected_groups = [True, True, True]
        self.group_rects = [None, None, None]
        self.start_btn_rect = None

        # These will be set after selection
        self.kana_list = []
        self.index = 0
        self.show_romaji = False

    def _is_basic(self, kana):
        return kana in (
            list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん") +
            list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
        )
    def _is_daku(self, kana):
        return kana in (
            list("がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ") +
            list("ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ")
        )
    def _is_combo(self, kana):
        return kana in (
            list("きゃきゅきょしゃしゅしょちゃちゅちょにゃにゅにょひゃひゅひょみゃみゅみょりゃりゅりょぎゃぎゅぎょじゃじゅじょびゃびゅびょぴゃぴゅぴょ") +
            list("キャキュキョシャシュショチャチュチョニャニュニョヒャヒュヒョミャミュミョリャリュリョギャギュギョジャジュジョビャビュビョピャピュピョ")
        )

    def _filtered_kana(self):
        filters = [f for sel, (_, f) in zip(self.selected_groups, self.kana_groups) if sel]
        if not filters:
            return []
        return [k for k in self.app.table.keys() if any(f(k) for f in filters)]

    def handle(self, event):
        if self.selecting:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for i, rect in enumerate(self.group_rects):
                    if rect and rect.collidepoint(pos):
                        self.selected_groups[i] = not self.selected_groups[i]
                if self.start_btn_rect and self.start_btn_rect.collidepoint(pos):
                    if any(self.selected_groups):
                        self.selecting = False
                        self.kana_list = self._filtered_kana()
                        random.shuffle(self.kana_list)
                        self.index = 0
                        self.show_romaji = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.change_scene(Menu(self.app))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.change_scene(Menu(self.app))
                elif event.key == pygame.K_RIGHT:
                    if self.kana_list:
                        self.index = (self.index + 1) % len(self.kana_list)
                        self.show_romaji = False
                elif event.key == pygame.K_LEFT:
                    if self.kana_list:
                        self.index = (self.index - 1) % len(self.kana_list)
                        self.show_romaji = False
                elif event.key == pygame.K_SPACE:
                    self.show_romaji = not self.show_romaji

    def draw(self, surf):
        surf.fill(BG)
        if self.selecting:
            draw_text(surf, "Flashcards", FONT_MD, ACCENT, center=(WIDTH//2, 120))
            y = 220
            self.group_rects = []
            for i, (label, _) in enumerate(self.kana_groups):
                checked = self.selected_groups[i]
                color = ACCENT if checked else MUTED
                # Center the group label horizontally
                rect = draw_text(surf, label, FONT_MD, color, center=(WIDTH//2, y), align="center")
                self.group_rects.append(rect)
                y += 70
            btn_color = OK if any(self.selected_groups) else MUTED
            self.start_btn_rect = draw_text(surf, "START", FONT_MD, btn_color, center=(WIDTH//2, int(HEIGHT * 0.8)))
            draw_text(surf, "ESC to cancel", FONT_SM, MUTED, center=(WIDTH//2, HEIGHT-28))
        else:
            draw_text(surf, "Flashcards (SPACE to flip)", FONT_SM, MUTED, topleft=(24, 20))
            if not self.kana_list:
                draw_text(surf, "No kana selected!", FONT_MD, WARN, center=(WIDTH//2, HEIGHT//2))
                return
            kana = self.kana_list[self.index]
            romaji = self.app.table[kana]
            draw_text(surf, kana, FONT_LG, WHITE, center=(WIDTH//2, HEIGHT//2 - 40))
            if self.show_romaji:
                draw_text(surf, romaji.upper(), FONT_MD, ACCENT, center=(WIDTH//2, HEIGHT//2 + 80))
            draw_text(surf, f"{self.index+1}/{len(self.kana_list)}", FONT_SM, MUTED, center=(WIDTH//2, HEIGHT-28))


class TypeMode(Scene):
    def __init__(self, app):
        self.app = app
        self.score = 0
        self.streak = 0
        self.feedback = ""
        self.feedback_timer = 0
        self.feedback_color = (255, 255, 255)
        self.input = InputLine()
        self.selecting = True
        self.kana_groups = [
            ("BASIC", self._is_basic),
            ("DAKUTEN & HANDAKUTEN", self._is_daku),
            ("COMBO KANA", self._is_combo),
            ("WORD", self._is_word),
        ]
        self.selected_groups = [True, True, True, False]
        self.group_rects = [None, None, None, None]
        self.start_btn_rect = None
        self.kana_list = []
        self.kana = None
        self.word_mode = False
        self.word_list = []
        self.word = None
        self.word_romaji = ""

    def _is_basic(self, kana):
        return kana in (
            list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
            + list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
        )

    def _is_daku(self, kana):
        return kana in (
            list("がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ")
            + list("ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ")
        )

    def _is_combo(self, kana):
        return kana in (
            list("きゃきゅきょしゃしゅしょちゃちゅちょにゃにゅにょひゃひゅひょみゃみゅみょりゃりゅりょぎゃぎゅぎょじゃじゅじょびゃびゅびょぴゃぴゅぴょ")
            + list("キャキュキョシャシュショチャチュチョニャニュニョヒャヒュヒョミャミュミョリャリュリョギャギュギョジャジュジョビャビュビョピャピュピョ")
        )

    def _is_word(self, kana):
        return False

    def _filtered_kana(self):
        filters = [f for sel, (_, f) in zip(self.selected_groups[:3], self.kana_groups[:3]) if sel]
        if not filters:
            return []
        return [k for k in self.app.table.keys() if any(f(k) for f in filters)]

    def _pick(self) -> str:
        prog = self.app.progress[self.app.script_name]
        items = [(k, choice_weight(int(prog.get(k, 1)))) for k in self.kana_list]
        total = sum(w for _, w in items)
        x = random.random() * total
        acc = 0
        for k, w in items:
            acc += w
            if x <= acc:
                return k
        return items[-1][0] if items else None

    def kana_to_romaji(self, word):
        table = self.app.table
        i = 0
        result = ""
        while i < len(word):
            if i + 1 < len(word) and word[i:i+2] in table:
                result += table[word[i:i+2]]
                i += 2
            elif word[i] in table:
                result += table[word[i]]
                i += 1
            else:
                result += word[i]
                i += 1
        return result

    def pick_word(self):
        self.word = random.choice(self.word_list)
        self.word_romaji = self.kana_to_romaji(self.word)

    def handle(self, event):
        if self.selecting:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for i, rect in enumerate(self.group_rects):
                    if rect and rect.collidepoint(pos):
                        self.selected_groups[i] = not self.selected_groups[i]
                if self.start_btn_rect and self.start_btn_rect.collidepoint(pos):
                    if any(self.selected_groups):
                        self.selecting = False
                        self.word_mode = self.selected_groups[3]
                        if self.word_mode:
                            self.word_list = WORDS.get(self.app.script_name, [])
                            if not self.word_list:
                                self.word = None
                                self.word_romaji = ""
                            else:
                                self.pick_word()
                        else:
                            self.kana_list = self._filtered_kana()
                            self.kana = self._pick()
                        self.input.text = ""
                        self.score = 0
                        self.streak = 0
                        self.feedback = ""
                        self.feedback_timer = 0
                        self.feedback_color = (255, 255, 255)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.change_scene(Menu(self.app))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.change_scene(Menu(self.app))
            res = self.input.handle(event)
            if res == "submit":
                guess = self.input.text.strip().lower().replace(" ", "")
                if self.word_mode:
                    correct = self.word_romaji.replace(" ", "")
                    if not self.word:
                        self.feedback = "No words available!"
                        self.feedback_color = (255, 255, 255)
                        self.feedback_timer = 60
                    elif guess == correct:
                        self.streak += 1
                        self.score = self.streak
                        self.feedback = "CORRECT"
                        self.feedback_color = OK
                    else:
                        self.streak = 0
                        self.score = 0
                        self.feedback = f"{self.word_romaji}"
                        self.feedback_color = WARN
                    self.feedback_timer = 45
                    if self.word_list:
                        self.pick_word()
                    self.input.text = ""
                else:
                    correct = self.app.table[self.kana]
                    script = self.app.script_name
                    if guess == correct:
                        self.streak += 1
                        self.score = self.streak
                        if self.score > self.app.progress["best_score"][script]:
                            self.app.progress["best_score"][script] = self.score
                        self.feedback = "CORRECT"
                        self.feedback_color = OK
                        self._bump_mastery(self.kana, +1)
                    else:
                        self.streak = 0
                        self.score = 0
                        self.feedback = f"{correct}"
                        self.feedback_color = WARN
                        self._bump_mastery(self.kana, -1)
                    self.feedback_timer = 45
                    save_progress(self.app.progress)
                    self.kana = self._pick()
                    self.input.text = ""

    def update(self, dt):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

    def draw(self, surf):
        surf.fill(BG)
        if self.selecting:
            draw_text(surf, "Type", FONT_MD, ACCENT, center=(WIDTH//2, 120))
            y = 220
            self.group_rects = []
            for i, (label, _) in enumerate(self.kana_groups):
                checked = self.selected_groups[i]
                color = ACCENT if checked else MUTED
                rect = draw_text(surf, label, FONT_MD, color, center=(WIDTH//2, y), align="center")
                self.group_rects.append(rect)
                y += 70
            btn_color = OK if any(self.selected_groups) else MUTED
            self.start_btn_rect = draw_text(surf, "START", FONT_MD, btn_color, center=(WIDTH//2, int(HEIGHT * 0.8)))
            draw_text(surf, "ESC to cancel", FONT_SM, MUTED, center=(WIDTH//2, HEIGHT-28))
        else:
            if self.word_mode:
                draw_text(surf, "Type — enter the romaji for the word", FONT_SM, MUTED, topleft=(24, 20))
            else:
                draw_text(surf, "Type — enter the romaji and press Enter", FONT_SM, MUTED, topleft=(24, 20))
            draw_text(surf, f"Score: {self.score}   Streak: {self.streak}", FONT_SM, MUTED, topleft=(24, 52))
            if not self.word_mode:
                best = self.app.progress["best_score"][self.app.script_name]
                draw_text(surf, f"Best: {best}", FONT_SM, WARN, topleft=(WIDTH - 180, 52))
            if self.word_mode:
                if not self.word:
                    draw_text(surf, "No words available!", FONT_MD, WARN, center=(WIDTH//2, HEIGHT//2))
                    return
                draw_text(surf, self.word, FONT_LG, WHITE, center=(WIDTH//2, HEIGHT//2 - 80))
            else:
                if not self.kana:
                    draw_text(surf, "No kana selected!", FONT_MD, WARN, center=(WIDTH//2, HEIGHT//2))
                    return
                draw_text(surf, self.kana, FONT_LG, WHITE, center=(WIDTH//2, HEIGHT//2 - 80))
            min_width = 220
            padding = 40
            shown = self.input.text.upper() + ("|" if self.input.cursor else " ")
            if self.word_mode and self.word:
                romaji = self.word_romaji.upper() if self.word_romaji else ""
                text_width = max(FONT_MD.size(romaji)[0], FONT_MD.size(shown)[0]) + padding
                box_width = max(min_width, text_width)
            else:
                text_width = FONT_MD.size(shown)[0] + padding
                box_width = max(min_width, text_width)
            input_rect = pygame.Rect(WIDTH//2 - box_width//2, HEIGHT//2 + 10, box_width, 60)
            self.input.draw(surf, input_rect)
            if self.feedback_timer > 0:
                draw_text(surf, self.feedback, FONT_MD, self.feedback_color, center=(WIDTH//2, 100))


# -----------------------------
# App wrapper
# -----------------------------
class App:
    def __init__(self):
        self.running = True
        self.script_name = "hiragana"  # or 'katakana'
        self.progress = load_progress()
        self.table = HIRAGANA
        self.scene: Scene = Menu(self)

    def toggle_script(self):
        if self.script_name == "hiragana":
            self.script_name = "katakana"
            self.table = KATAKANA
        else:
            self.script_name = "hiragana"
            self.table = HIRAGANA

    def change_scene(self, scene: Scene):
        self.scene = scene

    def run(self):
        while self.running:
            dt = CLOCK.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and isinstance(self.scene, Menu):
                    self.running = False
                else:
                    self.scene.handle(event)
            self.scene.update(dt)
            self.scene.draw(SCREEN)
            pygame.display.flip()
        pygame.quit()


def load_words():
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"hiragana": [], "katakana": []}

WORDS = load_words()


if __name__ == "__main__":
    App().run()