from lxml import etree
import requests
from io import BytesIO
import pandas
from zipfile import ZipFile


popoular_name_url = "https://uscode.house.gov/popularnames/popularnames.htm"
table3_zip_url = "https://uscode.house.gov/table3/table3-xml-bulk.zip"

if __name__ == "__main__":
    print("Downloading Popular Name List")
    popular_names = requests.get(popoular_name_url)

    print("Downloaded popularnames.htm", len(popular_names.content), "bytes")
    parser = etree.HTMLParser(huge_tree=True)
    tree   = etree.parse(BytesIO(popular_names.content), parser)
    
    items = tree.xpath("//div[@class='popular-name-table-entry']")
    
    print("Detected", len(items), "acts")
    
    res = [{
        "Name": item.getchildren()[0].text,
        "PubL": item.getchildren()[1].getchildren()[0].text,
    } for item in items if len(item.getchildren()) > 1 and item.getchildren()[1].text == "Pub. L. "]
    
    print("Detected", len(res), "PubL acts")
    
    pop_df = pandas.DataFrame.from_records(res)
    pop_df.to_excel("PopularNames.xlsx", index=False)
    print("Wrote PopularNames.xlx", len(pop_df), "rows")
    
    print("Downloading Table3 Zip")
    
    table3 = requests.get(table3_zip_url)
    print("Downloaded table3-xml-bulk.zip", len(table3.content), "bytes")
    with ZipFile(BytesIO(table3.content), 'r') as table3_zip:
        with table3_zip.open(table3_zip.namelist()[0]) as table3_xml:
            t3edit = etree.fromstring(table3_xml.read())
            rec = []
            acts = t3edit.xpath("//act")
            
            print("Detected", len(acts), "acts")
            for act in acts:
                act_base = {f"act_{key}": value for key, value in act.attrib.items()}
                act_children = act.getchildren()
                if act_children[0].tag != "num":
                    print("Detected Act without num", act_base["act_id"])
                else:
                    act_base["act_num"] = act_children[0].text
                    act_records = act.xpath("record")
                    for record in act_records:
                        rec.append(
                        {
                            **act_base,
                            **{f"record_{key}": value for key, value in record.attrib.items()},
                            **{f"record_{item.tag}":item.text for item in record.getchildren()}
                        })
                        
            t3_df = pandas.DataFrame.from_records(rec)
            t3_df.to_excel("Table3.xlsx", index=False)
            print("Wrote Table3.xlx", len(t3_df), "rows")