import requests
import tkinter as tk
from tkinter import messagebox

#  الاسعار الاحتياطية
# وضعت مقابل الدولار لتسهيل وضع عملات جديدة 
BACKUP_RATES_USD = {
    'USD': 1.0,            #بناءعلى بيانات موثوقة وصادرة يوم 3 مارس 2026
    'EUR': 0.874,       # يورو
    'GBP': 0.755,       # جنيه استرليني
    'JPY': 159.35,      # ين ياباني  
    'CHF': 0.789,      # فرنك سويسري
    'CAD': 1.34,       # دولار كندي
    'AUD': 1.42,       # دولاراسترالي
    'SYP': 12000,      # ليرة سورية (تقريبي) صعب للغاية بسبب الظروف الاقتصادية والسياسية في البلاد
    'JOD': 0.71,       # دينار اردني
    'IQD': 1310,       # دينار عراقي
    'EGP': 30.5,       # جنيه مصري
    'MAD': 10.2,       # درهم مغربي
    'SAR': 3.75,       # ريال سعودي
    'AED': 3.67,       # درهم اماراتي
}

# قائمة العملات المدعومة 
currencies = list(BACKUP_RATES_USD.keys())  

# دالة تجلب السعر الحالي من الانترنت
def get_exchange_rate(from_curr, to_curr):
    
    url = "https://api.frankfurter.app/latest"

    params = {
        'from': from_curr.upper(),
        'to': to_curr.upper()
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            print(f"Network error: status code {response.status_code}")
            return None
        data = response.json()
        if 'rates' not in data:
            print("Missing 'rates' in response")
            return None
        rate = data['rates'].get(to_curr.upper())
        return rate
    except Exception as e:
        print(f"Failed to get live rate: {e}")
        return None

#تحاول اولا الحصول على السعر الحالي ان فشل تستخدم الاحتياطي ان فشل ترجع فشل
def convert_currency(amount, from_curr, to_curr):

    # محاولة بالسعر الحالي
    live_rate = get_exchange_rate(from_curr, to_curr)
    if live_rate is not None:
        print("(Using real-time rate)")
        return amount * live_rate

    # في حال الفشل تدهب للاسعار الاحتياطية 
    print("Live rate not available, trying backup...")
    if from_curr in BACKUP_RATES_USD and to_curr in BACKUP_RATES_USD:
        # تحول من الاصلية للدولار ثم للمطلوب 
        amount_in_usd = amount / BACKUP_RATES_USD[from_curr]
        converted = amount_in_usd * BACKUP_RATES_USD[to_curr]
        print("(Using cached rate)")
        return converted
    else:
        print("No backup rate for this currency pair.")
        return None


def convert_gui():
    from_curr = clicked_from.get()
    to_curr = clicked_to.get()
    amount_str = entry_amount.get().strip()

    # التحقق من صحة المبلغ
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Error","Amount must be a valid number.")
        return

    result = convert_currency(amount, from_curr, to_curr)

 
    if result is not None:
        label_result.config(text=f"{amount} {from_curr} = {result:.2f} {to_curr}")
    else:
        label_result.config(text="Conversion error. Make sure currencies are valid.")


COLORS = {
    'bg': "#150C2D",           # خلفية النافذة 
    'frame_bg': "#261B4F",      # خلفية الاطار
    'label': "#CEDD48",         # لون النصوص
    'entry_bg': "#bab5b5",     #خلفية حقل ادخال المبلغ
    'entry_fg': "#050404",      # لون النص في حقل المبلغ
    'button_bg': "#c67b19",     # لون الزر 
    'button_fg': "#0d0e0d",     # لون نص الزر
    'button_hover': "#779367", 
    'result_fg': "#f1fbf1"      
}



window = tk.Tk()
window.title("Currency Converter")
window.geometry("550x450")
window.resizable(False, False)
window.configure(bg=COLORS['bg'])


label_title = tk.Label(
    window,
    text="Currency Converter",
    font=("Arial", 20, "bold"),
    bg=COLORS['bg'],
    fg=COLORS['label']
)
label_title.pack(pady=20)


main_frame = tk.Frame(
    window,
    bg=COLORS['frame_bg'],
    padx=20,
    pady=20,
    relief='groove',
    bd=1
)
main_frame.pack(pady=10, padx=20, fill='both', expand=True)

# العملة الاساس
label_from = tk.Label(
    main_frame,
   text="From:", 
    font=("Arial",20),
    bg=COLORS['frame_bg'],
    fg=COLORS['label']
)
label_from.grid(row=0, column=0, padx=10, pady=10, sticky='w')

clicked_from = tk.StringVar()
clicked_from.set("USD")  # القيمة الافتراضية
menu_from = tk.OptionMenu(main_frame, clicked_from, *currencies)
menu_from.config(
    font=("Arial",15 ),
    bg='white',
    fg='black',
    activebackground=COLORS['button_bg'],
    activeforeground='white',
    width=10
)
menu_from.grid(row=0, column=1, padx=10, pady=10)

# العملة المطلوبة 
label_to = tk.Label(
    main_frame,
     text="To:",  
    font=("Arial", 20),
    bg=COLORS['frame_bg'],
    fg=COLORS['label']
)
label_to.grid(row=1, column=0, padx=10, pady=10, sticky='w')

clicked_to = tk.StringVar()
clicked_to.set("EUR")
menu_to = tk.OptionMenu(main_frame, clicked_to, *currencies)
menu_to.config(
    font=("Arial", 15),
    bg='white',
    fg='black',
    activebackground=COLORS['button_bg'],
    activeforeground='white',
    width=10
)
menu_to.grid(row=1, column=1, padx=10, pady=10)


label_amount = tk.Label(
    main_frame,
    text="Amount:",
    font=("Arial", 20),
    bg=COLORS['frame_bg'],
    fg=COLORS['label']
)
label_amount.grid(row=2, column=0, padx=10, pady=10, sticky='w')

entry_amount = tk.Entry(
    main_frame,
    font=("Arial", 20),      
    width=15,                
    bg=COLORS['entry_bg'],
    fg=COLORS['entry_fg'],
    bd=1,
    relief='solid'
)
entry_amount.grid(row=2, column=1, padx=10, pady=10)
entry_amount.insert(0, " 5")  # قيمة افتراضية

# hover
def on_enter(e): 
    button_convert.config(bg=COLORS['button_hover'])

def on_leave(e):
    button_convert.config(bg=COLORS['button_bg'])

button_convert = tk.Button(
    main_frame,
    text="Convert", 

    font=("Arial", 15, "bold"),
    bg=COLORS['button_bg'],
    fg=COLORS['button_fg'],
    activebackground=COLORS['button_hover'],
    activeforeground='white',
    padx=15,
    pady=12,
    bd=0,
    cursor='hand2',
    command=convert_gui
)
button_convert.grid(row=3, column=1, columnspan=2, pady=12)
button_convert.bind("<Enter>", on_enter)
button_convert.bind("<Leave>", on_leave)


label_result = tk.Label(
    main_frame,
    text="",
    font=("Arial", 14, "bold"),
    bg=COLORS['frame_bg'],
    fg=COLORS['result_fg']
)
label_result.grid(row=4, column=0, columnspan=2, pady=10)

window.mainloop()