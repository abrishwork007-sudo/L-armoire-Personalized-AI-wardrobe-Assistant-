"""
╔══════════════════════════════════════════════════════╗
║           L ' a r m o i r e                         ║
║           AI Wardrobe Assistant — Python OOP         ║
╚══════════════════════════════════════════════════════╝
"""

import os
import random
import time

# ─────────────────────────────────────────────
# ANSI Color Codes for terminal styling
# ─────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    GOLD    = "\033[33m"
    CREAM   = "\033[97m"
    GREY    = "\033[90m"
    GREEN   = "\033[32m"
    RED     = "\033[31m"
    CYAN    = "\033[36m"
    MAGENTA = "\033[35m"
    BG_DARK = "\033[40m"

def gold(text):   return f"{Color.GOLD}{Color.BOLD}{text}{Color.RESET}"
def dim(text):    return f"{Color.DIM}{text}{Color.RESET}"
def bold(text):   return f"{Color.BOLD}{text}{Color.RESET}"
def green(text):  return f"{Color.GREEN}{text}{Color.RESET}"
def red(text):    return f"{Color.RED}{text}{Color.RESET}"
def grey(text):   return f"{Color.GREY}{text}{Color.RESET}"
def cyan(text):   return f"{Color.CYAN}{text}{Color.RESET}"


# ─────────────────────────────────────────────
# CLASS: WardrobeItem
# ─────────────────────────────────────────────
class WardrobeItem:
    _id_counter = 1

    def __init__(self, name: str, color: str, category: str):
        self.id       = WardrobeItem._id_counter
        self.name     = name
        self.color    = color
        self.category = category   # "tops" | "bottoms" | "shoes"
        WardrobeItem._id_counter += 1

    def __str__(self):
        return f"[{self.id}] {self.name} — {self.color}  {grey('(' + self.category + ')')}"


# ─────────────────────────────────────────────
# CLASS: Wardrobe
# ─────────────────────────────────────────────
class Wardrobe:
    def __init__(self):
        self.items = {"tops": [], "bottoms": [], "shoes": []}

    def add_item(self, item: WardrobeItem):
        self.items[item.category].append(item)
        print(green(f"  ✓ '{item.name}' added to {item.category}."))

    def remove_item(self, category: str, item_id: int) -> bool:
        for i, item in enumerate(self.items[category]):
            if item.id == item_id:
                removed = self.items[category].pop(i)
                print(green(f"  ✓ '{removed.name}' removed."))
                return True
        print(red("  ✗ Item not found."))
        return False

    def get_item_by_id(self, category: str, item_id: int):
        for item in self.items[category]:
            if item.id == item_id:
                return item
        return None

    def total_count(self):
        return sum(len(v) for v in self.items.values())

    def display(self):
        for category, item_list in self.items.items():
            print(f"\n  {gold('◆')} {bold(category.upper())}")
            if not item_list:
                print(grey("    (empty)"))
            else:
                for item in item_list:
                    print(f"    {item}")


# ─────────────────────────────────────────────
# CLASS: User
# ─────────────────────────────────────────────
class User:
    _id_counter = 1

    def __init__(self, name: str, password: str):
        self.id       = f"USR{User._id_counter:04d}"
        self.name     = name
        self.password = password
        self.wardrobe = Wardrobe()
        self.settings = {
            "notifications": True,
            "ai_suggestions": True,
            "public_profile": False,
        }
        User._id_counter += 1
        # Seed some default items
        self._seed_wardrobe()

    def _seed_wardrobe(self):
        defaults = [
            WardrobeItem("Classic White Shirt",    "White",     "tops"),
            WardrobeItem("Black Turtleneck",        "Black",     "tops"),
            WardrobeItem("Tailored Trousers",       "Charcoal",  "bottoms"),
            WardrobeItem("Denim Jeans",             "Indigo",    "bottoms"),
            WardrobeItem("Leather Oxford Shoes",    "Tan",       "shoes"),
        ]
        for item in defaults:
            self.wardrobe.items[item.category].append(item)

    def check_password(self, password: str) -> bool:
        return self.password == password


# ─────────────────────────────────────────────
# CLASS: StyleEvaluator  (AI logic simulation)
# ─────────────────────────────────────────────
class StyleEvaluator:

    COLOR_CLASHES = [
        ({"orange", "pink"}, "Orange and pink can overwhelm — try neutrals instead."),
        ({"red", "green"},   "Red and green clash sharply outside festive contexts."),
        ({"brown", "black"}, "Brown and black can muddy the palette — pick one dark tone."),
    ]

    GOOD_COMBOS = [
        ({"white", "black"},   "A timeless monochrome pairing — effortlessly elegant."),
        ({"white", "navy"},    "Classic nautical harmony — clean and polished."),
        ({"cream", "camel"},   "Tonal dressing at its finest — luxuriously cohesive."),
        ({"black", "charcoal"},"Tonal dark layering — sophisticated and sleek."),
        ({"beige", "white"},   "Soft neutrals create a refined, effortless look."),
        ({"ivory", "tan"},     "Warm neutrals — understated and elegant."),
    ]

    @staticmethod
    def evaluate(top: WardrobeItem, bottom: WardrobeItem, shoes: WardrobeItem) -> dict:
        colors = {
            top.color.lower(),
            bottom.color.lower(),
            shoes.color.lower()
        }

        score  = random.randint(55, 95)  # base score
        text   = ""
        tip    = ""
        verdict_type = "approved"

        # Check clashes
        for clash_set, clash_msg in StyleEvaluator.COLOR_CLASHES:
            if clash_set.issubset(colors):
                score = max(30, score - 30)
                text  = clash_msg
                verdict_type = "suggestion"
                tip   = "Try swapping one piece for a neutral like white, black, or beige."
                break

        # Check good combos
        for good_set, good_msg in StyleEvaluator.GOOD_COMBOS:
            if good_set.issubset(colors):
                score = min(98, score + 10)
                text  = good_msg
                verdict_type = "approved"
                tip   = "This pairing photographs beautifully. Accessorize in gold or silver."
                break

        if not text:
            if score >= 70:
                text = f"Your {top.color.lower()} {top.name.lower()} pairs well with the {bottom.color.lower()} {bottom.name.lower()}. The {shoes.color.lower()} shoes ground the look nicely."
                tip  = "A statement accessory would elevate this further."
                verdict_type = "approved"
            elif score >= 50:
                text = f"A decent foundation, but the color mix could be more intentional. The {shoes.color.lower()} shoes feel slightly disconnected."
                tip  = "Try swapping the shoes for a more neutral tone."
                verdict_type = "suggestion"
            else:
                text = "The combination feels mismatched. Consider rebuilding around one anchor color."
                tip  = "Start with a neutral base — white, black, or beige — and build from there."
                verdict_type = "suggestion"

        return {
            "score":   score,
            "type":    verdict_type,
            "text":    text,
            "tip":     tip,
        }


# ─────────────────────────────────────────────
# CLASS: AuthManager
# ─────────────────────────────────────────────
class AuthManager:
    def __init__(self):
        self.users: list[User] = []

    def signup(self, name: str, password: str):
        for u in self.users:
            if u.name.lower() == name.lower():
                print(red("  ✗ Username already exists."))
                return None
        user = User(name, password)
        self.users.append(user)
        print(green(f"  ✓ Account created. Welcome, {name}!"))
        return user

    def login(self, name: str, password: str):
        for u in self.users:
            if u.name.lower() == name.lower() and u.check_password(password):
                print(green(f"  ✓ Welcome back, {u.name}!"))
                return u
        print(red("  ✗ Invalid credentials."))
        return None


# ─────────────────────────────────────────────
# CLASS: LArmoireApp  (Main Application)
# ─────────────────────────────────────────────
class LArmoireApp:
    def __init__(self):
        self.auth     = AuthManager()
        self.user     = None          # currently logged in user
        self.selected = {"tops": None, "bottoms": None, "shoes": None}

    # ── Utilities ──────────────────────────────
    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def divider(self, char="─", width=54):
        print(gold(char * width))

    def header(self, title: str, subtitle: str = ""):
        self.clear()
        self.divider("═")
        print(gold(f"  ◆  L'armoire  ◆  ") + bold(title.upper()))
        if subtitle:
            print(dim(f"     {subtitle}"))
        self.divider("─")
        print()

    def pause(self):
        input(dim("\n  Press Enter to continue..."))

    def prompt(self, msg: str) -> str:
        return input(f"  {gold('›')} {msg}: ").strip()

    def loading(self, msg: str = "Curating your look"):
        print(f"\n  {gold('◆')} {msg}", end="", flush=True)
        for _ in range(3):
            time.sleep(0.4)
            print(gold(" ."), end="", flush=True)
        print()

    # ── Auth Screen ────────────────────────────
    def screen_auth(self):
        while not self.user:
            self.header("Your Personal Wardrobe", "Dress with intention.")
            print(f"  {gold('[1]')} Login")
            print(f"  {gold('[2]')} Sign Up")
            print(f"  {gold('[0]')} Exit")
            print()
            choice = self.prompt("Choose")

            if choice == "1":
                self.header("Login")
                name = self.prompt("Username")
                pwd  = self.prompt("Password")
                self.user = self.auth.login(name, pwd)
                self.pause()

            elif choice == "2":
                self.header("Create Account")
                name = self.prompt("Choose a username")
                pwd  = self.prompt("Choose a password")
                self.user = self.auth.signup(name, pwd)
                self.pause()

            elif choice == "0":
                self.clear()
                print(gold("\n  Au revoir. ◆\n"))
                exit()

    # ── Main Menu ──────────────────────────────
    def screen_main_menu(self):
        while True:
            sel_summary = ", ".join(
                f"{k}: {v.name}" if v else f"{k}: —"
                for k, v in self.selected.items()
            )
            self.header(f"Welcome, {self.user.name}", sel_summary)
            print(f"  {gold('[1]')}  My Closet        {grey('— browse & manage wardrobe')}")
            print(f"  {gold('[2]')}  Daily Look        {grey('— build & evaluate outfit')}")
            print(f"  {gold('[3]')}  Body Analysis     {grey('— get style type advice')}")
            print(f"  {gold('[4]')}  Settings          {grey('— account & preferences')}")
            print(f"  {gold('[0]')}  Sign Out")
            print()
            choice = self.prompt("Navigate")

            if   choice == "1": self.screen_closet()
            elif choice == "2": self.screen_daily_look()
            elif choice == "3": self.screen_body_analysis()
            elif choice == "4": self.screen_settings()
            elif choice == "0":
                self.user     = None
                self.selected = {"tops": None, "bottoms": None, "shoes": None}
                break

    # ── My Closet ──────────────────────────────
    def screen_closet(self):
        while True:
            self.header("My Closet", f"{self.user.wardrobe.total_count()} pieces in your wardrobe")
            self.user.wardrobe.display()
            print()
            self.divider()
            print(f"  {gold('[A]')} Add item   {gold('[R]')} Remove item")
            print(f"  {gold('[S]')} Select for outfit   {gold('[0]')} Back")
            print()
            choice = self.prompt("Action").upper()

            if choice == "A":
                self._add_item()
            elif choice == "R":
                self._remove_item()
            elif choice == "S":
                self._select_item()
            elif choice == "0":
                break

    def _add_item(self):
        self.header("Add New Piece")
        name  = self.prompt("Item name (e.g. Silk Blouse)")
        if not name: return
        color = self.prompt("Color / description (e.g. Ivory)")
        if not color: return
        print()
        for i, cat in enumerate(["tops", "bottoms", "shoes"], 1):
            print(f"  {gold(str(i))} {cat.capitalize()}")
        cat_choice = self.prompt("Category")
        cats = ["tops", "bottoms", "shoes"]
        if cat_choice in ("1","2","3"):
            category = cats[int(cat_choice) - 1]
            item = WardrobeItem(name, color, category)
            self.user.wardrobe.add_item(item)
        else:
            print(red("  ✗ Invalid category."))
        self.pause()

    def _remove_item(self):
        self.header("Remove Item")
        for i, cat in enumerate(["tops", "bottoms", "shoes"], 1):
            print(f"  {gold(str(i))} {cat.capitalize()}")
        cat_choice = self.prompt("Category")
        cats = ["tops", "bottoms", "shoes"]
        if cat_choice not in ("1","2","3"):
            print(red("  ✗ Invalid."))
            self.pause()
            return
        category = cats[int(cat_choice) - 1]
        for item in self.user.wardrobe.items[category]:
            print(f"    {item}")
        item_id = self.prompt("Enter Item ID to remove")
        if item_id.isdigit():
            self.user.wardrobe.remove_item(category, int(item_id))
        else:
            print(red("  ✗ Invalid ID."))
        self.pause()

    def _select_item(self):
        self.header("Select for Outfit")
        for i, cat in enumerate(["tops", "bottoms", "shoes"], 1):
            print(f"  {gold(str(i))} {cat.capitalize()}")
        cat_choice = self.prompt("Category")
        cats = ["tops", "bottoms", "shoes"]
        if cat_choice not in ("1","2","3"):
            print(red("  ✗ Invalid."))
            self.pause()
            return
        category = cats[int(cat_choice) - 1]
        items = self.user.wardrobe.items[category]
        if not items:
            print(red(f"  ✗ No items in {category}."))
            self.pause()
            return
        for item in items:
            print(f"    {item}")
        item_id = self.prompt("Enter Item ID to select")
        if item_id.isdigit():
            item = self.user.wardrobe.get_item_by_id(category, int(item_id))
            if item:
                self.selected[category] = item
                print(green(f"  ✓ '{item.name}' selected for {category}."))
            else:
                print(red("  ✗ Item not found."))
        self.pause()

    # ── Daily Look ─────────────────────────────
    def screen_daily_look(self):
        self.header("Daily Look", "Today's ensemble")
        print(f"  {bold('Selected Outfit:')}\n")

        all_selected = all(self.selected[c] for c in ["tops", "bottoms", "shoes"])

        for cat in ["tops", "bottoms", "shoes"]:
            item = self.selected[cat]
            status = f"{gold('◆')} {item.name} — {item.color}" if item else grey("  — not selected")
            print(f"  {cyan(cat.upper()):<20} {status}")

        print()

        if not all_selected:
            print(dim("  ← Go to My Closet and select one item from each category first."))
            self.pause()
            return

        choice = self.prompt("Generate style assessment? (y/n)").lower()
        if choice != "y":
            return

        self.loading("Evaluating your ensemble")
        result = StyleEvaluator.evaluate(
            self.selected["tops"],
            self.selected["bottoms"],
            self.selected["shoes"]
        )

        print()
        self.divider()
        score = result["score"]
        if score >= 70:
            score_color = green
            label = "High · Well Coordinated"
        elif score >= 50:
            score_color = gold
            label = "Mid · Needs Refinement"
        else:
            score_color = red
            label = "Low · Significant Clash"

        verdict_label = green("✓  Outfit Approved") if result["type"] == "approved" else gold("✦  Style Suggestion")
        print(f"\n  {verdict_label}")
        print(f"  {bold('Style Score:')} {score_color(str(score) + '/100')}  {grey(label)}")
        print()

        # Score bar
        bar_len  = 40
        filled   = int(score / 100 * bar_len)
        bar      = score_color("█" * filled) + grey("░" * (bar_len - filled))
        print(f"  [{bar}]")
        print()
        print(f"  {result['text']}")
        print()
        print(f"  {gold('Tip:')} {dim(result['tip'])}")
        self.divider()

        reset = self.prompt("\n  Reset outfit selection? (y/n)").lower()
        if reset == "y":
            self.selected = {"tops": None, "bottoms": None, "shoes": None}
            print(green("  ✓ Outfit reset."))
        self.pause()

    # ── Body Analysis ──────────────────────────
    def screen_body_analysis(self):
        self.header("Body Analysis", "Discover your style archetype")

        types = {
            "1": {
                "name":  "Hourglass",
                "tips":  "Defined waist styles — wrap dresses, belted coats, fitted tops.",
                "avoid": "Boxy silhouettes that hide your natural shape.",
            },
            "2": {
                "name":  "Rectangle",
                "tips":  "Create curves — peplum tops, A-line skirts, layered outfits.",
                "avoid": "Straight cuts that don't define the waist.",
            },
            "3": {
                "name":  "Triangle (Pear)",
                "tips":  "Balance upper body — statement tops, structured shoulders, A-line skirts.",
                "avoid": "Clingy fabrics on the lower half.",
            },
            "4": {
                "name":  "Inverted Triangle",
                "tips":  "Balance lower body — wide-leg trousers, A-line skirts, simple tops.",
                "avoid": "Heavy shoulder detail or structured blazers.",
            },
            "5": {
                "name":  "Apple / Round",
                "tips":  "Empire waist, V-necks, flowy fabrics that drape elegantly.",
                "avoid": "Tight waistbands or clingy midsection styles.",
            },
        }

        print(f"  Select your body type:\n")
        for key, val in types.items():
            print(f"  {gold(key)}  {val['name']}")
        print()
        choice = self.prompt("Choose")

        if choice in types:
            bt = types[choice]
            print()
            self.divider()
            print(f"\n  {gold('◆')} {bold('Your Style Archetype:')} {bt['name']}")
            print(f"\n  {bold('What works for you:')}")
            print(f"    {bt['tips']}")
            print(f"\n  {bold('What to avoid:')}")
            print(f"    {red(bt['avoid'])}")
            self.divider()
        else:
            print(red("  ✗ Invalid choice."))
        self.pause()

    # ── Settings ───────────────────────────────
    def screen_settings(self):
        while True:
            self.header("Settings", "Account & preferences")
            u = self.user
            print(f"  {bold('Full Name:')}       {u.name}")
            print(f"  {bold('User ID:')}         {u.id}")
            print(f"  {bold('Wardrobe Items:')}  {u.wardrobe.total_count()} pieces")
            print(f"  {bold('Membership:')}      {gold('◆ Premium')}")
            print()
            self.divider()
            print(f"\n  {bold('Preferences:')}\n")
            prefs = list(u.settings.items())
            for i, (key, val) in enumerate(prefs, 1):
                toggle = green("[ON] ") if val else grey("[OFF]")
                label  = key.replace("_", " ").title()
                print(f"  {gold(str(i))} {toggle} {label}")
            print()
            print(f"  {gold('[0]')} Back")
            print()
            choice = self.prompt("Toggle preference or 0 to go back")

            if choice == "0":
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(prefs):
                key = prefs[int(choice) - 1][0]
                u.settings[key] = not u.settings[key]
                status = "enabled" if u.settings[key] else "disabled"
                print(green(f"  ✓ {key.replace('_',' ').title()} {status}."))
                time.sleep(0.5)

    # ── Run ────────────────────────────────────
    def run(self):
        while True:
            self.screen_auth()
            if self.user:
                self.screen_main_menu()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = LArmoireApp()
    app.run()
