import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"

CHART_COLORS = [
    "#4F46E5",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#EF4444",
    "#8B5CF6",
    "#EC4899",
    "#6B7280"
]

from database import (
    get_expenses,
    delete_expense,
    add_expense,
    update_expense,

    get_income,
    add_income,
    update_income,
    delete_income,

    get_total_income,
    get_total_expense,
    get_monthly_expense,
    get_balance,
    get_expense_by_category,

    add_goal,
    get_active_goal,
    update_goal,
    delete_goal,
    update_saved_amount,
    complete_goal,
    has_active_goal,
)

# ==========================================
# APP SETTINGS
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# MAIN WINDOW
# ==========================================

app = ctk.CTk()

app.title("Expense Tracker")
app.geometry("1250x750")
app.minsize(1050, 650)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)


# This remembers which expense we selected
selected_expense_id = None

# ==========================================
# LOAD ICONS
# ==========================================

ICON_SIZE = (22, 22)

food_icon = ctk.CTkImage(
    light_image=Image.open("assets/food.png"),
    dark_image=Image.open("assets/food.png"),
    size=ICON_SIZE
)

travel_icon = ctk.CTkImage(
    light_image=Image.open("assets/travel.png"),
    dark_image=Image.open("assets/travel.png"),
    size=ICON_SIZE
)

shopping_icon = ctk.CTkImage(
    light_image=Image.open("assets/shopping.png"),
    dark_image=Image.open("assets/shopping.png"),
    size=ICON_SIZE
)

bills_icon = ctk.CTkImage(
    light_image=Image.open("assets/bills.png"),
    dark_image=Image.open("assets/bills.png"),
    size=ICON_SIZE
)

health_icon = ctk.CTkImage(
    light_image=Image.open("assets/health.png"),
    dark_image=Image.open("assets/health.png"),
    size=ICON_SIZE
)

entertainment_icon = ctk.CTkImage(
    light_image=Image.open("assets/entertainment.png"),
    dark_image=Image.open("assets/entertainment.png"),
    size=ICON_SIZE
)

education_icon = ctk.CTkImage(
    light_image=Image.open("assets/education.png"),
    dark_image=Image.open("assets/education.png"),
    size=ICON_SIZE
)

other_icon = ctk.CTkImage(
    light_image=Image.open("assets/other.png"),
    dark_image=Image.open("assets/other.png"),
    size=ICON_SIZE
)

income_png = ctk.CTkImage(
    light_image=Image.open("assets/income.png"),
    dark_image=Image.open("assets/income.png"),
    size=(36,36)
)

expense_png = ctk.CTkImage(
    light_image=Image.open("assets/expense.png"),
    dark_image=Image.open("assets/expense.png"),
    size=(36,36)
)

category_icons = {

    "Food": food_icon,

    "Travel": travel_icon,

    "Shopping": shopping_icon,

    "Bills": bills_icon,

    "Health": health_icon,

    "Entertainment": entertainment_icon,

    "Education": education_icon,

    "Other": other_icon

}

icon_files = {

            "Food": "assets/food.png",

            "Travel": "assets/travel.png",

            "Shopping": "assets/shopping.png",

            "Bills": "assets/bills.png",

            "Health": "assets/health.png",

            "Entertainment": "assets/entertainment.png",

            "Education": "assets/education.png",

            "Other": "assets/other.png"

    }

# ==========================================
# SIDEBAR
# ==========================================

sidebar = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=0
)

sidebar.grid(
    row=0,
    column=0,
    sticky="nsew"
)



sidebar.grid_propagate(False)


logo_label = ctk.CTkLabel(
    sidebar,
    text="💰 Expense\nTracker",
    font=ctk.CTkFont(
        size=26,
        weight="bold"
    )
)

logo_label.pack(
    pady=(40, 50)
)

# ==========================================
# MAIN CONTENT
# ==========================================

main_frame = ctk.CTkFrame(
    app,
    corner_radius=0
)

main_frame.grid(
    row=0,
    column=1,
    sticky="nsew"
)

main_frame.grid_columnconfigure(
    0,
    weight=1
)

main_frame.grid_rowconfigure(
    4,
    weight=1
)

content_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

content_frame.grid(
    row=0,
    column=0,
    rowspan=10,
    sticky="nsew"
)

content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_rowconfigure(4, weight=1)

# ==========================================
# TITLE
# ==========================================

title_label = ctk.CTkLabel(
    content_frame,
    text="Expense Dashboard",
    font=ctk.CTkFont(
        size=30,
        weight="bold"
    )
)

title_label.grid(
    row=0,
    column=0,
    padx=30,
    pady=(25, 10),
    sticky="w"
)

report_frame = ctk.CTkFrame(
    main_frame
)

expense_report_page = ctk.CTkFrame(main_frame)

income_report_page = ctk.CTkFrame(main_frame)

# ==========================================
# SAVINGS GOAL PAGE
# ==========================================

goal_page = ctk.CTkFrame(main_frame)

goal_page.grid(
    row=0,
    column=0,
    rowspan=10,
    sticky="nsew"
)

goal_page.grid_remove()

expense_report_page.grid(
    row=0,
    column=0,
    rowspan=10,
    sticky="nsew"
)

expense_report_page.grid_remove()

income_report_page.grid(
    row=0,
    column=0,
    rowspan=10,
    sticky="nsew"
)

income_report_page.grid_remove()

report_frame.grid(
    row=0,
    column=0,
    rowspan=10,
    sticky="nsew"
)


report_frame.grid_remove()

def show_expense_page():

    hide_all_pages()

    expense_report_page.grid(
        row=0,
        column=0,
        rowspan=10,
        sticky="nsew"
    )

    app.after(
        100,
        draw_expense_page
    )

def show_income_page():

    hide_all_pages()

    income_report_page.grid(
        row=0,
        column=0,
        rowspan=10,
        sticky="nsew"
    )
    app.after(100, draw_income_page)

def show_goal_page():

    hide_all_pages()

    goal_page.grid(
        row=0,
        column=0,
        rowspan=10,
        sticky="nsew"
    )

    app.after(
        100,
        draw_goal_page
    )

def hide_all_pages():

    content_frame.grid_remove()

    report_frame.grid_remove()

    expense_report_page.grid_remove()

    income_report_page.grid_remove()

    goal_page.grid_remove()

def show_dashboard():

    hide_all_pages()

    content_frame.grid(
        row=0,
        column=0,
        rowspan=10,
        sticky="nsew"
    )

def show_reports():

    hide_all_pages()

    report_frame.grid(
        row=0,
        column=0,
        rowspan=10,
        sticky="nsew"
    )

dashboard_button = ctk.CTkButton(
    sidebar,
    text="Dashboard",
    height=45,
    command=show_dashboard
)

dashboard_button.pack(
    padx=20,
    pady=10,
    fill="x"
)


expenses_button = ctk.CTkButton(
    sidebar,
    text="Expenses",
    height=45
)

expenses_button.pack(
    padx=20,
    pady=10,
    fill="x"
)


income_button = ctk.CTkButton(
    sidebar,
    text="Income",
    height=45
)

income_button.pack(
    padx=20,
    pady=10,
    fill="x"
)

reports_button = ctk.CTkButton(
    sidebar,
    text="Reports",
    height=45,
    command=show_reports
)

reports_button.pack(
    padx=20,
    pady=10,
    fill="x"
)

expense_title = ctk.CTkLabel(
    expense_report_page,
    text="🥧 Expenses Analytics",
    font=ctk.CTkFont(size=30, weight="bold")
)

expense_title.pack(pady=20)

ctk.CTkButton(
    expense_report_page,
    text="⬅ Back",
    width=120,
    height=38,
    corner_radius=12,
    command=show_reports
).pack(anchor="w", padx=20)

expense_graph = ctk.CTkComboBox(
    expense_report_page,
    values=[
        "Pie",
        "Donut",
        "Bar"
    ],
    command=lambda e: draw_expense_page()
)

expense_graph.set("Pie")

expense_graph.pack(pady=20)

expense_graph_frame = ctk.CTkFrame(
    expense_report_page
)

expense_graph_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=30
)

def draw_expense_page():

    for widget in expense_graph_frame.winfo_children():
        widget.destroy()

    data = get_expense_by_category()

    if not data:
        ctk.CTkLabel(
            expense_graph_frame,
            text="No Expense Data",
            font=ctk.CTkFont(size=22)
        ).pack(expand=True)
        return

    values = [float(row[1]) for row in data]

    # Main container
    body = ctk.CTkFrame(expense_graph_frame, fg_color="transparent")
    body.pack(fill="both", expand=True)

    # Left = Chart
    chart_frame = ctk.CTkFrame(body, fg_color="transparent")
    chart_frame.pack(side="left", fill="both", expand=True)

    # Right = Legend
    legend = ctk.CTkFrame(body, width=310)
    legend.pack(side="right", fill="y", padx=20, pady=20)
    legend.pack_propagate(False)

    chart_type = expense_graph.get()

    if chart_type in ["Pie", "Donut"]:
        fig = plt.Figure(figsize=(7.8, 7.8))
    else:
        fig = plt.Figure(figsize=(9.2,5.3))

    ax = fig.add_subplot(111)
    fig.subplots_adjust(
        left=0.08,
        right=0.98,
        top=0.92,
        bottom=0.15
    )
    fig.patch.set_facecolor("#141A26")

    ax.set_facecolor("#141A26")

    ax.tick_params(
        axis="both",
        colors="white",
        labelsize=10
    )

    ax.xaxis.label.set_color("white")

    ax.yaxis.label.set_color("white")

    ax.title.set_color("white")

    if chart_type == "Pie":

        wedges, _ = ax.pie(
            values,
            startangle=90,
            labels=None,
            radius=1.38,
            wedgeprops=dict(
                edgecolor="none",
                linewidth=0
            )
        )

        ax.set_aspect("equal")
        ax.set_xlim(-1.65, 1.65)
        ax.set_ylim(-1.65, 1.65)

        for wedge, row in zip(wedges, data):

            category = row[0]

            if category not in icon_files:
                continue

            image = Image.open(icon_files[category]).convert("RGBA")

            icon = OffsetImage(np.asarray(image), zoom=0.08)

            angle = (wedge.theta1 + wedge.theta2) / 2

            radius = 0.68

            x = radius * np.cos(np.deg2rad(angle))
            y = radius * np.sin(np.deg2rad(angle))

            ab = AnnotationBbox(
                icon,
                (x, y),
                frameon=True,
                bboxprops=dict(
                    edgecolor="white",
                    facecolor="white",
                    linewidth=2,
                    boxstyle="circle,pad=0.05"
                )
            )

            ax.add_artist(ab)

    elif chart_type == "Donut":

        wedges, _ = ax.pie(
            values,
            startangle=90,
            labels=None,
            radius=1.38,
           wedgeprops=dict(
                width=0.68,      # Bigger donut
                edgecolor="none",
                linewidth=0
            )
        )

        

        ax.set_aspect("equal")
        ax.set_xlim(-1.65, 1.65)
        ax.set_ylim(-1.65, 1.65)

        for wedge, row in zip(wedges, data):

            category = row[0]

            if category not in icon_files:
                continue

            image = Image.open(icon_files[category]).convert("RGBA")

            icon = OffsetImage(np.asarray(image), zoom=0.08)

            angle = (wedge.theta1 + wedge.theta2) / 2

            radius = 0.85

            x = radius * np.cos(np.deg2rad(angle))
            y = radius * np.sin(np.deg2rad(angle))

    elif chart_type == "Bar":

        categories = [row[0] for row in data]
        amounts = [float(row[1]) for row in data]

        bars = ax.bar(
            categories,
            amounts,
            width=0.50,
            color=CHART_COLORS[:len(categories)],
            edgecolor="none",
            zorder=3
        )

        ax.set_ylim(0, max(values) * 1.25)
        ax.margins(x=0.18)
        ax.set_ylabel("₹", fontsize=12)

        ax.tick_params(axis="x", labelsize=11)
        ax.tick_params(axis="y", labelsize=10)

        plt.setp(
            ax.get_xticklabels(),
            rotation=0,
            ha="center"
        )

        ax.grid(
            axis="y",
            color="#8A8A8A",
            linestyle=(0,(4,4)),
            linewidth=0.8,
            alpha=0.35
        )

        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.spines["left"].set_color("#666666")
        ax.spines["bottom"].set_color("#666666")

        ax.margins(x=0.08)

        ymax=max(amounts)*1.18
       
        for bar, category in zip(bars,categories):

            image = Image.open(icon_files[category]).convert("RGBA")

            icon = OffsetImage(
                np.asarray(image),
                zoom=0.06
            )

            ab=AnnotationBbox(
                icon,
                (
                    bar.get_x()+bar.get_width()/2,
                    bar.get_height()
                ),
                xybox=(0,-8),
                xycoords="data",
                boxcoords="offset points",
                frameon=False
            )

            ax.add_artist(ab)

    canvas = FigureCanvasTkAgg(
        fig,
        master=chart_frame
    )
            
    canvas.draw()
                
    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    for row in data:

        category = row[0]
        amount = float(row[1])

        item = ctk.CTkFrame(
            legend,
            fg_color="transparent"
        )
        item.pack(fill="x", pady= 10)

        ctk.CTkLabel(
            item,
            image=category_icons.get(category),
            text=""
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            item,
            text=category,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="left")

        ctk.CTkLabel(
            item,
            text=f"₹{amount:,.0f}",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="right")

def draw_income_page():

    for widget in income_report_page.winfo_children():
        widget.destroy()

    # Get data
    income = get_total_income()
    expense = get_total_expense()

    # Title
    ctk.CTkLabel(
        income_report_page,
        text="📊 Income vs Expense",
        font=ctk.CTkFont(size=30, weight="bold")
    ).pack(pady=20)

    # Back button
    ctk.CTkButton(
        income_report_page,
        text="⬅ Back",
        width=120,
        command=show_reports
    ).pack(anchor="w", padx=20)

    # Chart Frame
    chart_frame = ctk.CTkFrame(income_report_page)

    body = ctk.CTkFrame(
        income_report_page,
        fg_color="transparent"
    )
    body.pack(fill="both", expand=True)

    chart_frame = ctk.CTkFrame(
        body,
        fg_color="transparent"
    )

    chart_frame.pack(
        side="left",
        fill="both",
        expand=True
    )

    legend = ctk.CTkFrame(
        body,
        width=300
    )

    legend.pack(
        side="right",
        fill="y",
        padx=20,
        pady=20
    )

    legend.pack_propagate(False)

    fig = plt.Figure(figsize=(10.5,6.2))

    fig.subplots_adjust(
        left=0.08,
        right=0.98,
        top=0.92,
        bottom=0.15
    )

    ax = fig.add_subplot(111)

    fig.patch.set_facecolor("#141A26")

    ax.set_facecolor("#141A26")

    ax.tick_params(
        axis="both",
        colors="white",
        labelsize=11
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#666666")
    ax.spines["bottom"].set_color("#666666")

    ax.grid(
        axis="y",
        color="#8A8A8A",
        linestyle=(0, (4,4)),
        linewidth=0.8,
        alpha=0.35
    )

    ax.set_axisbelow(True)

    labels = ["Income", "Expense"]

    values = [income, expense]

    icon_paths = [
        "assets/income.png",
        "assets/expense.png"
    ]

    bars = ax.bar(
        labels,
        values,
        width=0.55,
        color=["#19C37D", "#FF4D57"],
        edgecolor="none",
        zorder=3
    )

    for bar, path in zip(bars, icon_paths):

        image = Image.open(path).convert("RGBA")

        icon = OffsetImage(
            np.asarray(image),
            zoom=0.08
        )

        ab = AnnotationBbox(
            icon,
            (
                bar.get_x() + bar.get_width()/2,
                bar.get_height()
            ),
            xybox=(0,8),
            xycoords="data",
            boxcoords="offset points",
            frameon=False
        )

        ax.add_artist(ab)

    for bar, value in zip(bars, values):
        ax.text(
        bar.get_x() + bar.get_width()/2,
        value + max(values)*0.08,
        f"₹{value:,.0f}",
        ha="center",
        va="bottom",
        color="white",
        fontsize=11,
        fontweight="bold"
    )

    canvas = FigureCanvasTkAgg(
        fig,
        master=chart_frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    balance = income - expense

    ctk.CTkLabel(
        legend,
        text="Summary",
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(pady=(30,25))

    income_card = ctk.CTkFrame(
        legend,
        corner_radius=12
    )

    income_card.pack(
        fill="x",
        padx=15,
        pady=10
    )

    ctk.CTkLabel(
        income_card,
        text="💰 Income",
        font=ctk.CTkFont(
            size=16,
            weight="bold"
        )
    ).pack(
        anchor="w",
        padx=15,
        pady=(12,4)
    )

    ctk.CTkLabel(
        income_card,
        text=f"₹{income:,.0f}",
        font=ctk.CTkFont(
            size=22,
            weight="bold"
        )
    ).pack(
        anchor="w",
        padx=15,
        pady=(0,12)
    )

    expense_card = ctk.CTkFrame(
        legend,
        corner_radius=12
    )

    expense_card.pack(
        fill="x",
        padx=15,
        pady=10
    )

    ctk.CTkLabel(
        expense_card,
        text="💸 Expense",
        font=ctk.CTkFont(
            size=16,
            weight="bold"
        )
    ).pack(
        anchor="w",
        padx=15,
        pady=(12,4)
    )

    ctk.CTkLabel(
        expense_card,
        text=f"₹{expense:,.0f}",
        font=ctk.CTkFont(
            size=22,
            weight="bold"
        )
    ).pack(
        anchor="w",
        padx=15,
        pady=(0,12)
    )

    balance_color = "#22C55E"

    if balance < 0:
        balance_color = "#EF4444"

    balance_card = ctk.CTkFrame(
        legend,
        corner_radius=12
    )

    balance_card.pack(
        fill="x",
        padx=15,
        pady=10
    )

    ctk.CTkLabel(
        balance_card,
        text="Balance",
        text_color=balance_color,
        font=ctk.CTkFont(
            size=16,
            weight="bold"
        )
    ).pack(
        anchor="w",
        padx=15,
        pady=(12,4)
    )

    balance_card.pack(
        fill="x",
        padx=15,
        pady=10
    )
    
    ctk.CTkLabel(
        balance_card,
        text=f"₹{balance:,.0f}",
        font=ctk.CTkFont(
            size=22,
            weight="bold"
        )
    ).pack(
            anchor="w",
            padx=15,
            pady=(0,12)
        )
    

def draw_goal_page():

    for widget in goal_page.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        goal_page,
        text="🎯 Savings Goal",
        font=ctk.CTkFont(
            size=30,
            weight="bold"
        )
    ).pack(pady=25)

    ctk.CTkButton(
        goal_page,
        text="⬅ Back",
        width=120,
        command=show_reports
    ).pack(anchor="w", padx=20)

    if not has_active_goal():

        ctk.CTkLabel(
            goal_page,
            text="No Savings Goal Yet",
            font=ctk.CTkFont(size=22)
        ).pack(pady=80)

        ctk.CTkButton(
            goal_page,
            text="+ Create Goal",
            width=220,
            height=45,
            command=open_goal_window
        ).pack()

        return

    goal = get_active_goal()

    if goal is None:
        return

    goal_card = ctk.CTkFrame(
        goal_page,
        corner_radius=15
    )

    target = float(goal[2])
    saved = float(goal[4])
    remaining = target - saved
    progress = saved / target if target > 0 else 0
    progress = max(0.0, min(1.0, progress))

    goal_card.pack(
        fill="x",
        padx=40,
        pady=30
    )

    progressbar = ctk.CTkProgressBar(goal_card)

    progressbar.pack(
            fill="x",
            padx=30,
            pady=20
    )
    
    progressbar.set(progress)
    ctk.CTkLabel(
            goal_card,
            text=f"{progress*100:.0f}% Completed"
    )

    ctk.CTkLabel(
        goal_card,
        text=f"🎯 {goal[1]}",
        font=ctk.CTkFont(
            size=26,
            weight="bold"
        )
    ).pack(pady=(20,10))

    ctk.CTkLabel(
            goal_card,
            text=f"Target : ₹{target:,.0f}",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(pady=(20,10))

    ctk.CTkLabel(
            goal_card,
            text=f"Saved : ₹{saved:,.0f}",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(pady=(20,10))

    ctk.CTkLabel(
            goal_card,
           text=f"Remaining : ₹{remaining:,.0f}",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(pady=(20,10))

def open_goal_window():

    goal_window = ctk.CTkToplevel(app)

    goal_window.title("Create Savings Goal")
    goal_window.geometry("500x520")
    goal_window.transient(app)
    goal_window.grab_set()

    ctk.CTkLabel(
        goal_window,
        text="🎯 Create Savings Goal",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=(20, 15))

    goal_name_entry = ctk.CTkEntry(
        goal_window,
        width=350,
        placeholder_text="Goal Name"
    )
    goal_name_entry.pack(pady=10)

    target_entry = ctk.CTkEntry(
        goal_window,
        width=350,
        placeholder_text="Target Amount"
    )
    target_entry.pack(pady=10)

    reason_entry = ctk.CTkTextbox(
        goal_window,
        width=350,
        height=120
    )
    reason_entry.pack(pady=10)

    def save_goal():

        goal_name = goal_name_entry.get().strip()

        target = target_entry.get().strip()

        reason = reason_entry.get("1.0", "end").strip()

        if goal_name == "":

            messagebox.showwarning(
                "Missing Goal",
                "Please enter a goal name."
            )

            return

        if target == "":

            messagebox.showwarning(
                "Missing Amount",
                "Please enter the target amount."
            )

            return

        try:

            target = float(target)

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter numbers only."
            )

            return

        if target <= 0:

            messagebox.showwarning(
                "Invalid Amount",
                "Amount must be greater than 0."
            )

            return

        recommended = target * 1.10

        try:
            add_goal(
            goal_name,
            target,
            recommended,
            0,
            reason,
            date.today()
        )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return

        messagebox.showinfo(
            "Success",
            "Goal Created!"
        )

        goal_window.destroy()

        draw_goal_page()

    ctk.CTkButton(
        goal_window,
        text="Create Goal",
        width=200,
        command=save_goal
    ).pack(pady=20)



# ==========================================
# ADD INCOME POPUP
# ==========================================

def open_income_window():

    # Create popup
    income_window = ctk.CTkToplevel(app)

    income_window.title("Add Income")
    income_window.geometry("450x500")
    income_window.resizable(False, False)

    # Keep popup connected to main app
    income_window.transient(app)
    income_window.grab_set()



# ==========================================
# DASHBOARD SUMMARY CARDS
# ==========================================

summary_frame = ctk.CTkFrame(
    content_frame,
    fg_color="transparent"
)

summary_frame.grid(
    row=1,
    column=0,
    padx=30,
    pady=10,
    sticky="ew"
)


# Make all 3 cards equal size

summary_frame.grid_columnconfigure(
    0,
    weight=1
)

summary_frame.grid_columnconfigure(
    1,
    weight=1
)

summary_frame.grid_columnconfigure(
    2,
    weight=1
)


# ==========================================
# BALANCE CARD
# ==========================================

balance_card = ctk.CTkFrame(
    summary_frame,
    height=130
)

balance_card.grid(
    row=0,
    column=0,
    padx=(0, 10),
    sticky="ew"
)


balance_title = ctk.CTkLabel(
    balance_card,
    text="TOTAL BALANCE",
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    )
)

balance_title.pack(
    anchor="w",
    padx=25,
    pady=(25, 5)
)

balance_label = ctk.CTkLabel(
    balance_card,
    text="₹0.00",
    font=ctk.CTkFont(
        size=28,
        weight="bold"
    )
)

balance_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 25)
)

# ==========================================
# INCOME CARD
# ==========================================

income_card = ctk.CTkFrame(
    summary_frame,
    height=130
)

income_card.grid(
    row=0,
    column=1,
    padx=10,
    sticky="ew"
)


income_title = ctk.CTkLabel(
    income_card,
    text="TOTAL INCOME",
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    )
)

income_title.pack(
    anchor="w",
    padx=25,
    pady=(25, 5)
)


income_label = ctk.CTkLabel(
    income_card,
    text="₹0.00",
    font=ctk.CTkFont(
        size=28,
        weight="bold"
    )
)

income_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 10)
)


add_income_button = ctk.CTkButton(
    income_card,
    text="+ Add Income",
    width=120,
    height=30,
    command=open_income_window
)

add_income_button.pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)

# ==========================================
# EXPENSE CARD
# ==========================================

expense_card = ctk.CTkFrame(
    summary_frame,
    height=130
)

expense_card.grid(
    row=0,
    column=2,
    padx=(10, 0),
    sticky="new"
)


expense_title = ctk.CTkLabel(
    expense_card,
    text="TOTAL EXPENSES",
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    )
)

expense_title.pack(
    anchor="w",
    padx=25,
    pady=(25, 5)
)


total_expense_label = ctk.CTkLabel(
    expense_card,
    text="₹0.00",
    font=ctk.CTkFont(
        size=28,
        weight="bold"
    )
)

total_expense_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 25)
)

# ==========================================
# ADD / EDIT FORM
# ==========================================

form_frame = ctk.CTkFrame(
    content_frame
)

form_frame.grid(
    row=2,
    column=0,
    padx=30,
    pady=10,
    sticky="ew"
)


for i in range(5):

    form_frame.grid_columnconfigure(
        i,
        weight=1
    )


# TITLE

title_entry = ctk.CTkEntry(
    form_frame,
    placeholder_text="Expense Title"
)

title_entry.grid(
    row=0,
    column=0,
    padx=10,
    pady=(20, 10),
    sticky="ew"
)


# CATEGORY

category_box = ctk.CTkComboBox(
    form_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Health",
        "Education",
        "Other"
    ]
)

category_box.set("Food")

category_box.grid(
    row=0,
    column=1,
    padx=10,
    pady=(20, 10),
    sticky="ew"
)


# AMOUNT

amount_entry = ctk.CTkEntry(
    form_frame,
    placeholder_text="Amount"
)

amount_entry.grid(
    row=0,
    column=2,
    padx=10,
    pady=(20, 10),
    sticky="ew"
)


# PAYMENT METHOD

payment_box = ctk.CTkComboBox(
    form_frame,
    values=[
        "Cash",
        "UPI",
        "Debit Card",
        "Credit Card",
        "Bank Transfer"
    ]
)

payment_box.set("Cash")

payment_box.grid(
    row=0,
    column=3,
    padx=10,
    pady=(20, 10),
    sticky="ew"
)


# DESCRIPTION

description_entry = ctk.CTkEntry(
    form_frame,
    placeholder_text="Description"
)

description_entry.grid(
    row=0,
    column=4,
    padx=10,
    pady=(20, 10),
    sticky="ew"
)


# ==========================================
# CLEAR FORM
# ==========================================

def clear_form():

    global selected_expense_id

    selected_expense_id = None
    

    title_entry.delete(
        0,
        "end"
    )

    amount_entry.delete(
        0,
        "end"
    )

    description_entry.delete(
        0,
        "end"
    )

    category_box.set(
        "Food"
    )

    payment_box.set(
        "Cash"
    )

    update_button.configure(
        state="disabled"
    )


# ==========================================
# TABLE FRAME
# ==========================================

table_frame = ctk.CTkFrame(
    content_frame,
)

table_frame.grid(
    row=4,
    column=0,
    padx=30,
    pady=(10, 30),
    sticky="nsew"
)


# ==========================================
# TABLE
# ==========================================

columns = (
    "ID",
    "Title",
    "Category",
    "Amount",
    "Date",
    "Payment",
    "Description"
)


expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)


for column in columns:

    expense_table.heading(
        column,
        text=column
    )


expense_table.column(
    "ID",
    width=50,
    anchor="center"
)

expense_table.column(
    "Title",
    width=130
)

expense_table.column(
    "Category",
    width=110
)

expense_table.column(
    "Amount",
    width=100
)

expense_table.column(
    "Date",
    width=100
)

expense_table.column(
    "Payment",
    width=120
)

expense_table.column(
    "Description",
    width=180
)


expense_table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ==========================================
# UPDATE DASHBOARD CARDS
# ==========================================

def update_dashboard():

    try:

        total_income = get_total_income()

        total_expense = get_total_expense()

        balance = get_balance()


        income_label.configure(
            text=f"₹{total_income:,.2f}"
        )


        total_expense_label.configure(
            text=f"₹{total_expense:,.2f}"
        )


        balance_label.configure(
            text=f"₹{balance:,.2f}"
        )


    except Exception as error:

        messagebox.showerror(
            "Dashboard Error",
            str(error)
        )

# ==========================================
# LOAD EXPENSES
# ==========================================

def load_expenses():

    # Delete old table rows

    for item in expense_table.get_children():

        expense_table.delete(
            item
        )


    try:

        expenses = get_expenses()

        total = 0


        for expense in expenses:

            # Add amount to total

            total += float(
                expense[3]
            )


            # Add expense to table

            expense_table.insert(
                "",
                "end",
                values=(
                    expense[0],
                    expense[1],
                    expense[2],
                    f"{float(expense[3]):.2f}",
                    expense[4],
                    expense[5],
                    expense[6]
                )
            )


        # Update total expense card

        total_expense_label.configure(
            text=f"₹{total:,.2f}"
        )


    except Exception as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )

# ==========================================
# ADD EXPENSE
# ==========================================

def save_expense():

    title = title_entry.get().strip()

    category = category_box.get()

    amount = amount_entry.get().strip()

    payment = payment_box.get()

    description = description_entry.get().strip()


    if title == "":

        messagebox.showwarning(
            "Missing Information",
            "Please enter an expense title."
        )

        return


    if amount == "":

        messagebox.showwarning(
            "Missing Information",
            "Please enter an amount."
        )

        return


    try:

        amount = float(
            amount
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid number."
        )

        return


    if amount <= 0:

        messagebox.showwarning(
            "Invalid Amount",
            "Amount must be greater than 0."
        )

        return

    try:

        add_expense(
            title,
            category,
            amount,
            date.today(),
            payment,
            description
        )

        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )

        clear_form()

        load_expenses()

        update_dashboard()

    except Exception as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ==========================================
# SELECT TABLE ROW
# ==========================================

def select_expense(event):

    global selected_expense_id


    selected = expense_table.selection()


    if not selected:

        return


    # Get selected row

    item = expense_table.item(
        selected[0]
    )


    values = item[
        "values"
    ]


    # Save Expense ID

    selected_expense_id = values[0]


    # Clear old form values

    title_entry.delete(
        0,
        "end"
    )

    amount_entry.delete(
        0,
        "end"
    )

    description_entry.delete(
        0,
        "end"
    )


    # Put selected expense into form

    title_entry.insert(
        0,
        values[1]
    )

    category_box.set(
        values[2]
    )

    amount_entry.insert(
        0,
        values[3]
    )

    payment_box.set(
        values[5]
    )

    description_entry.insert(
        0,
        values[6]
    )


    # Enable update button

    update_button.configure(
        state="normal"
    )


expense_table.bind(
    "<<TreeviewSelect>>",
    select_expense
)
    
# ==========================================
# UPDATE EXPENSE
# ==========================================

def edit_expense():

    global selected_expense_id


    if selected_expense_id is None:

        messagebox.showwarning(
            "No Expense Selected",
            "Please select an expense first."
        )

        return


    title = title_entry.get().strip()

    category = category_box.get()

    amount = amount_entry.get().strip()

    payment = payment_box.get()

    description = description_entry.get().strip()


    if title == "":

        messagebox.showwarning(
            "Missing Information",
            "Please enter an expense title."
        )

        return


    try:

        amount = float(
            amount
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid amount."
        )

        return


    try:

        update_expense(
            selected_expense_id,
            title,
            category,
            amount,
            date.today(),
            payment,
            description
        )


        messagebox.showinfo(
            "Success",
            "Expense updated successfully!"
        )


        clear_form()

        load_expenses()

        update_dashboard()

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )
# ==========================================
# DELETE EXPENSE
# ==========================================

def remove_expense():

    global selected_expense_id


    if selected_expense_id is None:

        messagebox.showwarning(
            "No Expense Selected",
            "Please select an expense from the table first."
        )

        return


    answer = messagebox.askyesno(
        "Delete Expense",
        "Are you sure you want to delete this expense?"
    )


    if answer:

        try:

            delete_expense(
                selected_expense_id
            )


            messagebox.showinfo(
                "Deleted",
                "Expense deleted successfully!"
            )


            clear_form()

            load_expenses()

            update_dashboard()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

        

# ==========================================
# BUTTON AREA
# ==========================================

button_frame = ctk.CTkFrame(
    form_frame,
    fg_color="transparent"
)

button_frame.grid(
    row=1,
    column=0,
    columnspan=5,
    padx=10,
    pady=(5, 20),
    sticky="ew"
)


# ADD BUTTON

add_button = ctk.CTkButton(
    button_frame,
    text="+ Add Expense",
    command=save_expense
)

add_button.pack(
    side="left",
    padx=5
)


# UPDATE BUTTON

update_button = ctk.CTkButton(
    button_frame,
    text="Update Expense",
    command=edit_expense,
    state="disabled"
)

update_button.pack(
    side="left",
    padx=5
)


# DELETE BUTTON

delete_button = ctk.CTkButton(
    button_frame,
    text="Delete Expense",
    command=remove_expense
)

delete_button.pack(
    side="left",
    padx=5
)


# CLEAR BUTTON

clear_button = ctk.CTkButton(
    button_frame,
    text="Clear",
    command=clear_form
)

clear_button.pack(
    side="left",
    padx=5
)

# ==========================================
# REPORTS TITLE
# ==========================================

report_title = ctk.CTkLabel(
    report_frame,
    text="Reports",
    font=ctk.CTkFont(
        size=30,
        weight="bold"
    )
)

report_title.pack(
    anchor="w",
    padx=30,
    pady=(20,10)
)

# ==========================================
# REPORT MENU
# ==========================================

reports_body = ctk.CTkFrame(report_frame)

reports_body.pack(fill="both", expand=True, padx=40, pady=30)

reports_body.grid_columnconfigure((0,1), weight=1)
reports_body.grid_rowconfigure((0,1,2), weight=1)

goal_card = ctk.CTkFrame(reports_body)

goal_card.grid(
        row=1,
        column=1,
        padx=20,
        pady=20,
        sticky="nsew"
    )

ctk.CTkLabel(
        goal_card,
        text="🎯 Savings Goal",
        font=ctk.CTkFont(
            size=22,
            weight="bold"
        )
    ).pack(pady=(35,20))

ctk.CTkLabel(
        goal_card,
        text="Track your savings\nand reach your dream.",
        justify="center",
        text_color="gray70"
    ).pack(pady=(0,20))

ctk.CTkButton(
        goal_card,
        text="Open Goal →",
        width=220,
        height=45,
        command=show_goal_page
    ).pack(pady=(0,35))


expense_card = ctk.CTkFrame(reports_body)
expense_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(
    expense_card,
    text="🥧 Expenses by Category",
    font=ctk.CTkFont(size=22, weight="bold")
).pack(pady=(35,20))

ctk.CTkLabel(
    expense_card,
    text="Analyze your spending\nacross categories.",
    justify="center",
    text_color="gray70",
    font=ctk.CTkFont(size=14)
).pack(pady=(0,20))

ctk.CTkLabel(
    expense_card,
    text="🥧 Pie    🍩 Donut    📊 Bar",
    font=ctk.CTkFont(size=14)
).pack(pady=(0,20))

ctk.CTkButton(
    expense_card,
    text="View Analytics →",
    width=250,
    height=45,
    corner_radius=12,
    command=show_expense_page
).pack(pady=(0,35))

income_card = ctk.CTkFrame(reports_body)
income_card.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(
    income_card,
    text="📊 Income vs Expense",
    font=ctk.CTkFont(size=22, weight="bold")
).pack(pady=(35,20))

ctk.CTkLabel(
    income_card,
    text="Compare your income\nand expenses.",
    justify="center",
    text_color="gray70",
    font=ctk.CTkFont(size=14)
).pack(pady=(0,20))

ctk.CTkLabel(
    income_card,
    text="📊 Bar   📈 Trend",
    font=ctk.CTkFont(size=14)
).pack(pady=(0,20))

ctk.CTkButton(
    income_card,
    text="View Analytics →",
    width=250,
    height=45,
    corner_radius=12,
    command=show_income_page
).pack(pady=(0,35))

monthly_card = ctk.CTkFrame(reports_body)
monthly_card.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(
    monthly_card,
    text="📈 Monthly Spending",
    font=ctk.CTkFont(size=22, weight="bold")
).pack(pady=(35,20))

ctk.CTkButton(
    monthly_card,
    text="Open Report",
    width=220,
    height=45
).pack(pady=(0,35))

wallet_card = ctk.CTkFrame(reports_body)
wallet_card.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(
    wallet_card,
    text="💰 Wallet Balance",
    font=ctk.CTkFont(size=22, weight="bold")
).pack(pady=(35,20))

ctk.CTkButton(
    wallet_card,
    text="Open Report",
    width=220,
    height=45
).pack(pady=(0,35))

# ==========================================
# START
# ==========================================

load_expenses()

update_dashboard()

app.mainloop()