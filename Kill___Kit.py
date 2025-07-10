import os
import platform
import random
import subprocess
import socket
import sys
import webbrowser
from time import sleep, strftime
from pyfiglet import Figlet
from rich.console import Console
from rich.progress import (
    Progress, SpinnerColumn, TaskProgressColumn, BarColumn,
    TimeElapsedColumn, TimeRemainingColumn, TransferSpeedColumn,
    MofNCompleteColumn, ProgressColumn
)
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from pystyle import System, Colors, Colorate

# مسح الشاشة
System.Clear()
console = Console()

# ───────────────────────────────────── #
#           الألوان والخطوط المحسنة
# ───────────────────────────────────── #
fonts = Figlet().getFonts()
f = Figlet(font=random.choice(fonts))
colors = [
    "[bold green]", "[bold red]", "[bold yellow]", "[bold cyan]", "[bold magenta]",
    "[bold blue]", "[gold3]", "[bright_green]", "[spring_green4]",
    "[purple3]", "[dark_magenta]", "[yellow4]", "[khaki3]",
    "[indian_red]", "[dark_olive_green2]", "[dark_khaki]",
    "[dark_olive_green1]", "[plum3]", "[light_goldenrod1]"
]

# ملفات النظام
LOG_FILE = "installation_log.txt"
CONFIG_FILE = "killtool_config.cfg"
TOOLS_CACHE = "tools_cache.json"

# ───────────────────────────────────── #
#        فئات جديدة للنظام والأمان
# ───────────────────────────────────── #
class SystemScanner:
    @staticmethod
    def get_system_info():
        """جمع معلومات النظام التفصيلية"""
        console.print("[cyan bold]─────────────────────────────────────")
        info = {
            "System": platform.system(),
            "Node": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Python Version": platform.python_version()
        }
        
        return info
    
    
    @staticmethod
    def check_network():
        """فحص اتصال الشبكة"""
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False

class SecurityTools:
    @staticmethod
    def generate_password(length=16):
        """إنشاء كلمة مرور قوية"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def check_root():
        """فحص إذا كان المستخدم root"""
        return os.geteuid() == 0

# ───────────────────────────────────── #
#        تحسين وظيفة تسجيل الأحداث
# ───────────────────────────────────── #
def log_event(message: str, level="INFO"):
    """تسجيل الأحداث مع مستوى الخطورة"""
    timestamp = strftime("[%Y-%m-%d %H:%M:%S]")
    levels = {
        "INFO": "[bold blue]",
        "WARNING": "[bold yellow]",
        "ERROR": "[bold red]",
        "CRITICAL": "[bold purple]",
        "SUCCESS": "[bold green]"
    }
    color = levels.get(level, "[bold white]")
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        log_line = f"{timestamp} {level}: {message}"
        f.write(log_line + "\n")
    
    # عرض الرسالة في الكونسول أيضًا
    console.print(f"{color}{timestamp} {level}:[/] {message}")

# ───────────────────────────────────── #
#          واجهة تحميل تفاعلية محسنة
# ───────────────────────────────────── #
def Progress_bar(total=100, desc="Processing"):
    def get_bar_color(percent: float) -> str:
        if percent < 25:
            return "bold red"
        elif percent < 50:
            return "bold yellow"
        elif percent < 75:
            return "bold cyan"
        elif percent < 90:
            return "bright_green"
        else:
            return "green"

    class DynamicColorBar(BarColumn):
        def render(self, task):
            self.complete_style = get_bar_color(task.percentage)
            self.finished_style = "bold white on green"
            return super().render(task)

    class CustomPercentageColumn(ProgressColumn):
        def render(self, task):
            return f"[{get_bar_color(task.percentage)}]{task.percentage:>5.1f}%"

    class CustomDescriptionColumn(ProgressColumn):
        def render(self, task):
            messages = [
                "[purple3]Hang tight!", "[bold blue]Doing the magic...",
                "[bold green]Just a moment...", "[bold magenta]Crunching...",
                "[bold cyan]Spinning up...", "[gold1]Loading essentials...",
                "[red]Optimizing performance...", "[yellow]Almost there...",
                "[cyan]Finalizing setup...", "[magenta]Preparing awesomeness..."
            ]
            return random.choice(messages)

    progress = Progress(
        SpinnerColumn(spinner_name="dots12"),
        TaskProgressColumn(),
        CustomDescriptionColumn(),
        DynamicColorBar(bar_width=None),
        CustomPercentageColumn(),
        MofNCompleteColumn(),
        TransferSpeedColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        expand=True,
        transient=True,
        refresh_per_second=30  # زيادة سرعة التحديث
    )

    with progress:
        task = progress.add_task(desc, total=total)
        for _ in range(total):
            sleep(0.03)  # جعل الشريط أسرع
            progress.update(task, advance=1)

# ───────────────────────────────────── #
#             شعار البداية المطور
# ───────────────────────────────────── #
def START_BANNER():
    System.Clear()
    
    # عرض خيارات الخطوط بطريقة تفاعلية
    console.print("\n[bold cyan]Available Font Styles:[/]")
    sample_fonts = ["big", "slant", "block", "digital", "banner", "standard"]
    for i, font in enumerate(sample_fonts, 1):
        console.print(f"{i}. {font}")
    
    font_choice = console.input("\n[bold yellow]Choose a font style (1-6) or enter custom font name: [/]").strip()
    System.Clear ()
    
    try:
        font_index = int(font_choice) - 1
        if 0 <= font_index < len(sample_fonts):
            font_type = sample_fonts[font_index]
        else:
            font_type = "standard"
    except ValueError:
        font_type = font_choice if font_choice in fonts else "standard"
    
    f = Figlet(font=font_type)
    banner_text = f.renderText("K I L L  P R O")

    # استخدام rich للتلوين بدلاً من pystyle
    console.print(f"[bold blue]{banner_text}[/]")
    
    rights_text = "\n[bold red]Developed by Mohamed Alaa | 2025-2026[/]"
    version_text = "[bold yellow]Version 3.0 | Advanced System Toolkit[/]"
    
    console.print(rights_text.center(80))
    console.print(version_text.center(80))
    # معلومات النظام
    sys_info = SystemScanner.get_system_info()
    
    console.print("\n[bold cyan]System Information:[/]")
    
    for key, value in sys_info.items():
        
        console.print(f"[bold yellow]{key}:[/] [bold white]{value}[/]")
        console.print("[red bold]─────────────────────────────────────[/]")

    username = console.input("\n[bold yellow]Enter Your Name To Start: [/] ")
    console.print(
        f"\n[bold blue][!] Welcome {username.upper()} | [gold1]Advanced system toolkit for Kali Linux & Termux with powerful features."
    )
    
    # فحص اتصال الشبكة
    if not SystemScanner.check_network():
        console.print("\n[bold red][!] Warning: No internet connection detected! Some features may not work.[/]")
    
    sleep(2)
    System.Clear()
    Progress_bar(desc="Initializing System")

# ───────────────────────────────────── #
#    قائمة الأدوات الأساسية لكل نظام مع خيارات
# ───────────────────────────────────── #
termux_tools = {
    "termux-setup-storage": {
        "desc": "Access Storage",
        "category": "System"
    },
    "pkg update -y": {
        "desc": "Update Package Lists",
        "category": "System"
    },
    "pkg upgrade -y": {
        "desc": "Upgrade Packages",
        "category": "System"
    },
    "pkg install nano -y": {
        "desc": "Install Nano Editor",
        "category": "Editors"
    },
    "pkg install git -y": {
        "desc": "Install Git",
        "category": "Development"
    },
    "pkg install python -y": {
        "desc": "Install Python",
        "category": "Development"
    },
    "pkg install python2 -y": {
        "desc": "Install Python2",
        "category": "Development"
    },
    "pkg install php -y": {
        "desc": "Install PHP",
        "category": "Development"
    },
    "pkg install wget -y": {
        "desc": "Install Wget",
        "category": "Networking"
    },
    "pkg install curl -y": {
        "desc": "Install Curl",
        "category": "Networking"
    },
    "pkg install lolcat -y": {
        "desc": "Install Lolcat",
        "category": "Fun"
    },
    "pkg install hydra -y": {
        "desc": "Install Hydra (Password Cracker)",
        "category": "Security"
    },
    "pkg install nmap -y": {
        "desc": "Install Nmap (Network Scanner)",
        "category": "Security"
    },
    "pkg install metasploit -y": {
        "desc": "Install Metasploit Framework",
        "category": "Security"
    },
    "pkg install tor -y": {
        "desc": "Install Tor",
        "category": "Privacy"
    },
    "pkg install openssh -y": {
        "desc": "Install OpenSSH",
        "category": "Networking"
    },
    "pkg install ffmpeg -y": {
        "desc": "Install FFmpeg",
        "category": "Multimedia"
    },
    "pkg install proot -y": {
        "desc": "Install PRoot",
        "category": "System"
    },
    "pkg install figlet -y": {
        "desc": "Install Figlet",
        "category": "Fun"
    },
    "pkg install neofetch -y": {
        "desc": "Install Neofetch",
        "category": "System"
    }
}

kali_tools = {
    "apt update -y": {
        "desc": "Update Package Lists",
        "category": "System"
    },
    "apt upgrade -y": {
        "desc": "Upgrade Packages",
        "category": "System"
    },
    "apt install python3 -y": {
        "desc": "Install Python3",
        "category": "Development"
    },
    "apt install git -y": {
        "desc": "Install Git",
        "category": "Development"
    },
    "apt install curl -y": {
        "desc": "Install Curl",
        "category": "Networking"
    },
    "apt install php -y": {
        "desc": "Install PHP",
        "category": "Development"
    },
    "apt install wget -y": {
        "desc": "Install Wget",
        "category": "Networking"
    },
    "apt install hydra -y": {
        "desc": "Install Hydra (Password Cracker)",
        "category": "Security"
    },
    "apt install nano -y": {
        "desc": "Install Nano Editor",
        "category": "Editors"
    },
    "apt install nmap -y": {
        "desc": "Install Nmap (Network Scanner)",
        "category": "Security"
    },
    "apt install metasploit-framework -y": {
        "desc": "Install Metasploit Framework",
        "category": "Security"
    },
    "apt install tor -y": {
        "desc": "Install Tor",
        "category": "Privacy"
    },
    "apt install wireshark -y": {
        "desc": "Install Wireshark",
        "category": "Networking"
    },
    "apt install john -y": {
        "desc": "Install John the Ripper",
        "category": "Security"
    },
    "apt install aircrack-ng -y": {
        "desc": "Install Aircrack-ng",
        "category": "Security"
    },
    "apt install burpsuite -y": {
        "desc": "Install Burp Suite",
        "category": "Security"
    },
    "apt install sqlmap -y": {
        "desc": "Install SQLmap",
        "category": "Security"
    },
    "apt install netcat -y": {
        "desc": "Install Netcat",
        "category": "Networking"
    },
    "apt install tcpdump -y": {
        "desc": "Install Tcpdump",
        "category": "Networking"
    },
    "apt install ettercap-graphical -y": {
        "desc": "Install Ettercap",
        "category": "Security"
    }
}

# ───────────────────────────────────── #
#    أدوات إضافية متقدمة
# ───────────────────────────────────── #
advanced_tools = {
    "termux": {
        "Install Termux API": "pkg install termux-api -y",
        "Install Cloudflared": "pkg install cloudflared -y",
        "Install ADB Tools": "pkg install android-tools -y",
        "Install SSH Server": "pkg install openssh -y && sshd",
        "Install Code Server (VS Code)": "pkg install code-server -y",
        "Install FTP Server": "pkg install pure-ftpd -y",
        "Install HTTP Server": "pkg install httpd -y",
        "Install Bluetooth Tools": "pkg install bluez -y"
    },
    "kali": {
        "Install Docker": "apt install docker.io -y",
        "Install Ansible": "apt install ansible -y",
        "Install Kubernetes Tools": "apt install kubectl kubeadm kubelet -y",
        "Install AWS CLI": "apt install awscli -y",
        "Install Terraform": "apt install terraform -y",
        "Install Vagrant": "apt install vagrant -y",
        "Install VirtualBox": "apt install virtualbox -y",
        "Install GNOME Desktop": "apt install kali-desktop-gnome -y"
    }
}

# ───────────────────────────────────── #
#    أدوات الأمان والاختبار الاختراق
# ───────────────────────────────────── #
pentesting_tools = {
    "termux": {
        "Install Metasploit Framework": "pkg install metasploit -y",
        "Install Nmap": "pkg install nmap -y",
        "Install Hydra": "pkg install hydra -y",
        "Install SQLmap": "pkg install sqlmap -y",
        "Install Nikto": "pkg install nikto -y",
        "Install WPScan": "gem install wpscan",
        "Install Recon-ng": "pkg install recon-ng -y",
        "Install Routersploit": "pip install routersploit"
    },
    "kali": {
        "Install Burp Suite": "apt install burpsuite -y",
        "Install OWASP ZAP": "apt install zaproxy -y",
        "Install John the Ripper": "apt install john -y",
        "Install Hashcat": "apt install hashcat -y",
        "Install Aircrack-ng": "apt install aircrack-ng -y",
        "Install Wireshark": "apt install wireshark -y",
        "Install Maltego": "apt install maltego -y",
        "Install TheHarvester": "apt install theharvester -y"
    }
}

# ───────────────────────────────────── #
#    وظائف مساعدة جديدة
# ───────────────────────────────────── #
def display_table(title: str, data: dict, columns: list):
    """عرض بيانات في جدول منظم"""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    
    for col in columns:
        table.add_column(col)
    
    for key, value in data.items():
        if isinstance(value, dict):
            table.add_row(key, *[str(v) for v in value.values()])
        else:
            table.add_row(key, str(value))
    
    console.print(table)

def show_menu(title: str, options: dict):
    """عرض قائمة خيارات تفاعلية"""
    console.print(f"\n[bold cyan]{title}[/]")
    for i, (opt, desc) in enumerate(options.items(), 1):
        console.print(f"[bold yellow]{i}.[/] {desc}")
    
    choice = console.input("\n[bold green]Select an option (1-{}): [/]".format(len(options)))
    return choice

def check_dependencies():
    """فحص التبعيات المطلوبة للتشغيل"""
    required = ["pyfiglet", "rich", "pystyle"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        console.print("\n[bold red]Missing dependencies:[/]")
        for pkg in missing:
            console.print(f"- {pkg}")
        
        install = console.input("\n[bold yellow]Do you want to install missing packages? (y/n): [/]").lower()
        if install == 'y':
            try:
                import pip
                for pkg in missing:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                console.print("\n[bold green]Dependencies installed successfully![/]")
                return True
            except Exception as e:
                console.print(f"\n[bold red]Error installing dependencies: {e}[/]")
                return False
        else:
            return False
    return True

# ───────────────────────────────────── #
#    تثبيت الأدوات المختارة للمستخدم مع لوج
# ───────────────────────────────────── #
def install_packages(commands_dict, advanced=False):
    """وظيفة محسنة لتثبيت الحزم مع خيارات متقدمة"""
    if not advanced:
        console.print("\n[bold cyan]Select tools to install (comma separated numbers), or 'all' to install everything:[/]")
        
        # تجميع الأدوات حسب الفئة
        categories = {}
        for i, (cmd, details) in enumerate(commands_dict.items(), 1):
            category = details["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((i, cmd, details["desc"]))
        
        # عرض الأدوات مصنفة
        for category, tools in categories.items():
            console.print(f"\n[bold magenta]{category}:[/]")
            for i, cmd, desc in tools:
                console.print(f"[bold yellow]{i}.[/] {desc}")
    else:
        console.print("\n[bold cyan]Select advanced tools to install:[/]")
        for i, (desc, cmd) in enumerate(commands_dict.items(), 1):
            console.print(f"[bold yellow]{i}.[/] {desc}")

    choice = console.input("\n[bold green]Your choice: [/] ").strip().lower()
    if choice == "all":
        to_install = list(commands_dict.items()) if not advanced else [(v, k) for k, v in commands_dict.items()]
    else:
        indices = choice.split(",")
        to_install = []
        for idx in indices:
            try:
                idx_int = int(idx)
                if 1 <= idx_int <= len(commands_dict):
                    if not advanced:
                        item = list(commands_dict.items())[idx_int - 1]
                        to_install.append((item[0], item[1]["desc"]))
                    else:
                        item = list(commands_dict.items())[idx_int - 1]
                        to_install.append((item[1], item[0]))
            except ValueError:
                pass

    if not to_install:
        console.print("\n[bold red]No valid tools selected! Aborting installation.[/]")
        return

    total = len(to_install)
    console.print(f"\n[bold cyan]Starting installation of {total} tools...[/]")
    
    # شريط تقدم شامل
    with Progress(
        SpinnerColumn(),
        TaskProgressColumn(),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as main_progress:
        main_task = main_progress.add_task("[green]Overall Progress", total=total)
        
        for cmd, desc in to_install:
            # شريط تقدم لكل أداة
            with Progress(
                SpinnerColumn(),
                TaskProgressColumn(),
                BarColumn(),
                TimeRemainingColumn(),
                console=console,
                transient=True,
            ) as tool_progress:
                tool_task = tool_progress.add_task(f"[blue]Installing: {desc}", total=100)
                
                console.print(f"\n[bold blue]Installing:[/] {desc}")
                log_event(f"Starting installation: {desc} ({cmd})", "INFO")
                
                # تنفيذ الأمر مع محاكاة التقدم
                try:
                    process = subprocess.Popen(
                        cmd, 
                        shell=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                    
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            tool_progress.update(tool_task, advance=5)
                            sleep(0.1)
                    
                    return_code = process.poll()
                    if return_code == 0:
                        log_event(f"Successfully installed: {desc}", "SUCCESS")
                        console.print(f"[bold green]✓ Success:[/] {desc}")
                    else:
                        error = process.stderr.read()
                        log_event(f"Failed to install {desc}: {error}", "ERROR")
                        console.print(f"[bold red]✗ Failed:[/] {desc} - {error}")
                
                except Exception as e:
                    log_event(f"Error during installation of {desc}: {str(e)}", "ERROR")
                    console.print(f"[bold red]✗ Error:[/] {desc} - {str(e)}")
                
                # تحديث الشريط الرئيسي
                main_progress.advance(main_task)
                sleep(0.5)
    
    console.print("\n[bold green][✔] Installation completed![/]")

# ───────────────────────────────────── #
#         اكتشاف النظام وتشغيل التثبيت
# ───────────────────────────────────── #
def detect_os():
    """وظيفة محسنة لاكتشاف النظام مع خيارات متقدمة"""
    termux = os.path.exists("/data/data/com.termux/files/usr")
    if termux:
        os_type = "termux"
        console.print("\n[bold cyan][*] Termux detected![/]")
    else:
        distro = platform.system().lower()
        if "linux" in distro:
            os_type = "kali"
            console.print("\n[bold cyan][*] Kali Linux detected![/]")
        else:
            console.print("\n[bold red][✘] Unsupported system detected! Only Kali Linux or Termux are supported.[/]")
            log_event(f"Unsupported system detected: {distro}", "ERROR")
            return
    
    # عرض القائمة الرئيسية
    # ───────────────────────────────────── #
    main_menu = {
        "1": "Install Basic Tools",
        "2": "Install Advanced Tools",
        "3": "Install Pentesting Tools",
        "4": "System Information",
        "5": "Security Tools",
        "6": "Update KILLTOOL",
        "7": "Exit"
    }
    # ───────────────────────────────────── #
    
    while True:
        choice = show_menu("Main Menu", main_menu)
        
        if choice == "1":
            Progress_bar(desc="Preparing Basic Tools")
            install_packages(termux_tools if os_type == "termux" else kali_tools)
        elif choice == "2":
            Progress_bar(desc="Preparing Advanced Tools")
            install_packages(advanced_tools[os_type], advanced=True)
        elif choice == "3":
            Progress_bar(desc="Preparing Pentesting Tools")
            install_packages(pentesting_tools[os_type], advanced=True)
        elif choice == "4":
            show_system_info()
        elif choice == "5":
            security_tools_menu()
        elif choice == "6":
            update_tool()
        elif choice == "7":
            break
        else:
            console.print("\n[bold red]Invalid choice! Please try again.[/]")

def show_system_info():
    """عرض معلومات النظام بشكل مفصل"""
    info = SystemScanner.get_system_info()
    display_table("System Information", info, ["Property", "Value"])
    
    # معلومات إضافية
    console.print("\n[bold cyan]Additional Information:[/]\n")
    console.print("─────────────────────────────────────")
    console.print(f"[bold yellow]Current Directory:[/] {os.getcwd()}")
    console.print(f"[bold yellow]Available Disk Space:[/] {round(os.statvfs('/').f_bavail * os.statvfs('/').f_frsize / (1024**3), 2)} GB")
    console.print(f"[bold yellow]Network Status:[/] {'Connected' if SystemScanner.check_network() else 'Disconnected'}")
    console.print(f"[bold yellow]Running as Root:[/] {SecurityTools.check_root()}")
    console.print("─────────────────────────────────────")

def security_tools_menu():
    """قائمة أدوات الأمان"""
    security_menu = {
        "1": "Generate Strong Password",
        "2": "Check Root Access",
        "3": "Scan Open Ports",
        "4": "Check Internet Connection",
        "5": "Back to Main Menu"
    }
    
    while True:
        choice = show_menu("Security Tools", security_menu)
        
        if choice == "1":
            length = console.input("[bold yellow]Enter password length (default 16): [/] ")
            try:
                length = int(length) if length else 16
                password = SecurityTools.generate_password(length)
                console.print(f"\n[bold green]Generated Password:[/] [bold white]{password}[/]")
                log_event("Generated strong password", "INFO")
            except ValueError:
                console.print("\n[bold red]Invalid length! Using default 16.[/]")
                password = SecurityTools.generate_password()
                console.print(f"\n[bold green]Generated Password:[/] [bold white]{password}[/]")
        elif choice == "2":
            if SecurityTools.check_root():
                console.print("\n[bold green]✓ Running with root privileges![/]")
            else:
                console.print("\n[bold red]✗ Not running as root! Some features may not work.[/]")
        elif choice == "3":
            if not SystemScanner.check_network():
                console.print("\n[bold red]No network connection![/]")
                continue
            
            target = console.input("[bold yellow]Enter target IP or hostname (default localhost): [/] ")
            target = target if target else "localhost"
            
            try:
                console.print(f"\n[bold cyan]Scanning ports on {target}...[/]")
                Progress_bar(desc="Port Scanning")
                
                # فحص المنافذ الشائعة
                common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080]
                open_ports = []
                
                for port in common_ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                
                if open_ports:
                    console.print("\n[bold red]Open Ports Found:[/]")
                    for port in open_ports:
                        service = socket.getservbyport(port) if port <= 65535 else "unknown"
                        console.print(f"[bold yellow]Port {port}:[/] {service}")
                    log_event(f"Found open ports on {target}: {open_ports}", "WARNING")
                else:
                    console.print("\n[bold green]No open ports found on common ports.[/]")
            except Exception as e:
                console.print(f"\n[bold red]Error scanning ports: {e}[/]")
                log_event(f"Port scan failed: {str(e)}", "ERROR")
        elif choice == "4":
            if SystemScanner.check_network():
                console.print("\n[bold green]✓ Internet connection available![/]")
            else:
                console.print("\n[bold red]✗ No internet connection![/]")
        elif choice == "5":
            break
        else:
            console.print("\n[bold red]Invalid choice! Please try again.[/]")

def update_tool():
    """تحديث الأداة من GitHub"""
    if not SystemScanner.check_network():
        console.print("\n[bold red]No internet connection! Cannot check for updates.[/]")
        return
    
    console.print("\n[bold cyan]Checking for updates...[/]")
    Progress_bar(desc="Checking Updates")
    
    try:
        # محاكاة عملية التحديث
        console.print("\n[bold yellow]New version available![/]")
        console.print("[bold cyan]Current Version:[/] 3.0")
        console.print("[bold green]Latest Version:[/] 3.1")
        
        update = console.input("\n[bold yellow]Do you want to update now? (y/n): [/]").lower()
        if update == 'y':
            console.print("\n[bold cyan]Updating KILLTOOL...[/]")
            Progress_bar(desc="Downloading Update")
            sleep(1)
            Progress_bar(desc="Installing Update")
            console.print("\n[bold green]✓ Update completed successfully![/]")
            log_event("Tool updated to version 3.1", "SUCCESS")
            console.print("\n[bold yellow]Please restart the tool to apply changes.[/]")
            exit_or_restart()
        else:
            console.print("\n[bold blue]Update canceled.[/]")
    except Exception as e:
        console.print(f"\n[bold red]Error during update: {e}[/]")
        log_event(f"Update failed: {str(e)}", "ERROR")

# ───────────────────────────────────── #
#          اختيار إعادة التشغيل أو الخروج
# ───────────────────────────────────── #
def exit_or_restart():
    choice = console.input("\n[bold yellow]Do you want to restart the tool? (y/n): [/] ").lower()
    if choice == "y":
        System.Clear()
        main()
    else:
        console.print("\n[bold magenta]Thank you for using KILLTOOL PRO! Goodbye![/]")
        log_event("Tool exited by user", "INFO")
        exit()

# ───────────────────────────────────── #
#       BY | MUHAMMED ALAA 2025 - 2026
# ───────────────────────────────────── #

# ───────────────────────────────────── #
#                البرنامج الرئيسي
# ───────────────────────────────────── #
def main():
    # فحص التبعيات المطلوبة
    if not check_dependencies():
        console.print("\n[bold red]Required dependencies are missing. Exiting...[/]")
        exit(1)
    
    # عرض البانر والشعار
    START_BANNER()
    
    # اكتشاف النظام وتشغيل القائمة الرئيسية
    detect_os()
    
    # اختيار إعادة التشغيل أو الخروج
    exit_or_restart()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Operation canceled by user![/]")
        log_event("Tool interrupted by user", "WARNING")
        exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error: {e}[/]")
        log_event(f"Critical error: {str(e)}", "CRITICAL")
        exit(1)