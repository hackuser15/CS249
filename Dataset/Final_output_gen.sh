
textItemIds = "/Users/avneet/Desktop/CS249/Dataset/output_textid.csv"
prodIds = "/Users/avneet/Desktop/CS249/Dataset/prod_ids.csv"

paste -d ',' $textItemIds $prodIds > Final_result.csv

