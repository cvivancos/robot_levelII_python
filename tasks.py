"""
from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from RPA.Tables import Tables
import os
from pathlib import Path
from RPA.Browser.Selenium import Selenium
"""

"""
#img_folder = os.environ["/images_files"]
#pdf_folder = os.environ["/pdf_files"]
#output_folder = os.environ["/output"]
output = Path("./output")
orders_file = output / "orders.csv"
#zip_file = output_folder+"/pdf_archive.zip"

@task
def order_robots_from_RobotSpareBin():
    ""Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    ""
    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()

    orders = get_orders()
    for row in orders:
        close_the_annoying_modal()
        fill_the_form(row)
    # archive_receipts()



def open_robot_order_website():
     ""Navegar a la URL""
     browser.goto("https://robotsparebinindustries.com/#/robot-order")


def close_the_annoying_modal():
    page=browser.page()
    #page.wait_for_selector("class:alert-buttons")
    page.click("button:text('OK')")


def get_orders():
    #orders_file=Files.create_workbook
    HTTP().download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True, target_file=orders_file)
        #excel = Files()
    #excel.open_workbook(orders_file)
    table = Tables().read_table_from_csv(orders_file, header=True)
    #table = excel.read_csv_as_table(orders_file, header=True)
    #excel.close_workbook()
    return table


def fill_the_form(myrow):
    page=browser.page()
    page.select_option("#head", myrow["Head"])
    #page.check("#from-check-input", myrow["Body"])
    page.check("#id-body-"+str(myrow['Body']))
    page.type("#/html/body/div/div/div[1]/div/div[1]/form/div[3]/input", myrow["Legs"])
    #page.fill("#xpath://html/body/div/div/div[1]/div/div[1]/form/div[3]/input", myrow["Legs"])
    page.fill("#address", myrow["Address"])
"""
from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
import shutil

@task
def order_robot_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo=200)
    open_robot_order_website()
    download_orders_file()
    fill_form_with_csv_data()
    archive_receipts()
    clean_up()


def open_robot_order_website():
    """Navigates to the given URL and clicks on pop up"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()
    page.click('text=OK')

def download_orders_file():
    """Downloads the orders file from the give URL"""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)

def order_another_bot():
    """Clicks on order another button to order another bot"""
    page = browser.page()
    page.click("#order-another")

def clicks_ok():
    """Clicks on ok whenever a new order is made for bots"""
    page = browser.page()
    page.click('text=OK')

def fill_and_submit_robot_data(order):
    """Fills in the robot order details and clicks the 'Order' button"""
    page = browser.page()
    head_names = {
        "1" : "Roll-a-thor head",
        "2" : "Peanut crusher head",
        "3" : "D.A.V.E head",
        "4" : "Andy Roid head",
        "5" : "Spanner mate head",
        "6" : "Drillbit 2000 head"
    }
    head_number = order["Head"]
    page.select_option("#head", head_names.get(head_number))
    page.click('//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{0}]/label'.format(order["Body"]))
    page.fill("input[placeholder='Enter the part number for the legs']", order["Legs"])
    page.fill("#address", order["Address"])
    while True:
        page.click("#order")
        order_another = page.query_selector("#order-another")
        if order_another:
            pdf_path = store_receipt_as_pdf(int(order["Order number"]))
            screenshot_path = screenshot_robot(int(order["Order number"]))
            embed_screenshot_to_receipt(screenshot_path, pdf_path)
            order_another_bot()
            clicks_ok()
            break

def store_receipt_as_pdf(order_number):
    """This stores the robot order receipt as pdf"""
    page = browser.page()
    order_receipt_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf_path = "output/receipts/{0}.pdf".format(order_number)
    pdf.html_to_pdf(order_receipt_html, pdf_path)
    return pdf_path

def fill_form_with_csv_data():
    """Read data from csv and fill in the robot order form"""
    csv_file = Tables()
    robot_orders = csv_file.read_table_from_csv("orders.csv")
    for order in robot_orders:
        fill_and_submit_robot_data(order)
          
def screenshot_robot(order_number):
    """Takes screenshot of the ordered bot image"""
    page = browser.page()
    screenshot_path = "output/screenshots/{0}.png".format(order_number)
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path

def embed_screenshot_to_receipt(screenshot_path, pdf_path):
    """Embeds the screenshot to the bot receipt"""
    pdf = PDF()
    pdf.add_watermark_image_to_pdf(image_path=screenshot_path, 
                                   source_path=pdf_path, 
                                   output_path=pdf_path)
    
def archive_receipts():
    """Archives all the receipt pdfs into a single zip archive"""
    lib = Archive()
    lib.archive_folder_with_zip("./output/receipts", "./output/receipts.zip")

def clean_up():
    """Cleans up the folders where receipts and screenshots are saved."""
    shutil.rmtree("./output/receipts")
    shutil.rmtree("./output/screenshots")