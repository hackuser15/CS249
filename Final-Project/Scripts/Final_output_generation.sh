
#textItemIds = "../Intermediate_files/output_textid.csv"
#prodIds = "../Intermediate_files/prod_ids.csv"

#paste -d ',' $textItemIds $prodIds > ../Intermediate_files/Final_result.csv
paste -d ',' ../Intermediate_files/output_textids.csv ../Intermediate_files/prod_ids.csv > ../Intermediate_files/Final_result.csv
echo "complete"
