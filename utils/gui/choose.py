import win32gui
import flet as ft
import time
import threading
from flet_core import MainAxisAlignment, CrossAxisAlignment
from align_angle import main as align_angle
from diver import DivergentUniverse, version
from utils.gui.common import show_snack_bar, Page, list_handles
from utils.diver.config import config as config_diver
from utils.diver.args import args
from utils.log import my_print as print
from utils.log import print_exc
from utils.globals import init_status,ui_stream

def choose_view(page: Page):
    def change_all_button(value: bool = True):
        cnt = 0
        for i in page.views[0].controls[0].controls:
            if isinstance(i, ft.FilledButton):
                if cnt <= 1:
                    i.disabled = value
                    cnt += 1
                else:
                    i.disabled = False
        page.update()

    def run(func, *args, **kwargs):
        try:
            change_all_button()
            res = func(*args, **kwargs)
            change_all_button(False)
            return res
        except Exception:
            print("Error: 运行函数时出现错误")
            print_exc()
        finally:
            change_all_button(False)

    def angle(_e):
        init_status.value = True
        show_snack_bar(page, "开始校准，请切换回游戏（¬､¬）", ft.colors.GREEN)
        res = run(align_angle,status = init_status)
        if res == 1:
            show_snack_bar(page, "校准成功（＾∀＾●）", ft.colors.GREEN)
        else:
            if init_status.value:
                show_snack_bar(page, "校准失败（⊙.⊙）", ft.colors.RED)
        try:
            guind = list_handles('AutoDivergentUniverse')
            win32gui.SetForegroundWindow(guind)
        except:
            pass

    def start(_e, name):
        init_status.value = True
        show_snack_bar(page, "开始运行，请切换回游戏（＾∀＾●）", ft.colors.GREEN)
        if name == 'diver':
            args.cpu = int(config_diver.cpu_mode)
            page.su = run(
                DivergentUniverse, # func
                int(config_diver.debug_mode), # args
                int(config_diver.max_run),
                int(config_diver.speed_mode),
                init_status=init_status,
            )
        if init_status.value: # 如果已经完成初始化,则启动主程序
            show_snack_bar(page, "完成初始化", ft.colors.GREEN)
            run(page.su.start)
            try:
                guind = list_handles('AutoDivergentUniverse')
                win32gui.SetForegroundWindow(guind)
            except:
                pass
            if page.su is not None:
                run(page.su.stop)
        else:
            page.su = None # 如果没有完成初始化,则清空缓存
        show_snack_bar(page, "已退出自动化", ft.colors.GREEN)

    def stops(_e):
        show_snack_bar(page, "停止运行（>∀<）", ft.colors.GREEN)
        try:
            init_status.value = False
        except:
            pass
        if page.su is not None:
            run(page.su.stop)

    def go_config(_e, name):
        page.go("/config_"+name)

    def go_about(e=None):
        dlg = ft.AlertDialog(
            title=ft.Text("差分宇宙自动化"),
            content=ft.Text(
                "Welcome to https://github.com/Waverider02/ADU"
            ),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def go_test(e=None):
        init_status.value = True
        show_snack_bar(page, "开始测试，请切换回游戏（＾∀＾●）", ft.colors.GREEN)
        args.cpu = int(config_diver.cpu_mode)
        page.su = run(
            DivergentUniverse,
            int(config_diver.debug_mode),
            int(config_diver.max_run),
            int(config_diver.speed_mode),
            init_status=init_status,
        )
        if init_status.value:
            run(page.su.screen_test)
            if page.su is not None:
                run(page.su.stop)
            show_snack_bar(page, "已完成截图测试", ft.colors.GREEN)
        else:
            page.su = None # 如果没有完成初始化,则清空缓存

    layout = ft.Column(
                    controls = [
                        ft.Container(
                            content=ft.Text(
                                "AutoDivergentUniverse",
                                size=50,
                            ),
                        ),
                        ft.Container(
                            content=ft.Text(
                                version+' @ '+'Changed by Waverider02',
                                size=20,
                            ),
                        ),
                        ft.Container(
                            content=ft.Text(
                                "开源项目: ADU (https://github.com/Waverider02/ADU)",
                                size=20,
                            ),
                        ),
                        ft.Container(),
                        ft.Row([
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.ADD_TASK),
                                    ft.Text("校准", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=angle,
                            width=120,
                        ),
                        ft.Container(),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.TRACK_CHANGES),
                                    ft.Text("测试", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=go_test,
                            width=120,
                        ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,),
                        ft.Container(),
                        ft.Row([
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.LOGIN),
                                    ft.Text("运行", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=lambda e: start(e, 'diver'),
                            width=120,
                        ),
                        ft.Container(),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.STOP),
                                    ft.Text("停止", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=stops,
                            width=120,
                        ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,),
                        ft.Container(),
                        ft.Row([
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.INFO),
                                    ft.Text("关于", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=go_about,
                            width=120,
                        ),
                        ft.Container(),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.SETTINGS),
                                    ft.Text("设置", weight=ft.FontWeight.W_600),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            on_click=lambda e: go_config(e, 'diver'),
                            width=120,
                        ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,),
                    ],alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER)
    
    session_text = ft.Text(
                            ui_stream.text_str,
                            size=16,
                            weight=ft.FontWeight.NORMAL,
                            color=ft.colors.BLUE,
                            width=600,
                            height=200,
                            selectable=True,
                        )
    
    session = ft.Column([ft.Container(),
                        ft.Container(border=ft.border.all(1)),
                        session_text,
                        ft.Container(border=ft.border.all(1)),],alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER)
    
    # View
    page.views.append(ft.View("/",[layout,session]))
    page.update()

    def refresh_loop():
        while not ui_stream.stop:
            session_text.value = ui_stream.text_str
            page.update()
            time.sleep(0.2)

    threading.Thread(target=refresh_loop,daemon=True).start() # 子线程,每0.2s刷新页面
