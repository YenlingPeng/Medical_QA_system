# -*- coding: utf-8 -*-

def main():
  # Load csv file
  df_commonhealth = pd.read_csv("./csvs/commonhealth_revised.csv")
  df_nowhealth = pd.read_csv("./csvs/nowhealth_revised.csv")
  df_udn = pd.read_csv("./csvs/udn_revised.csv")
  df_jah = pd.read_csv("./csvs/jah_revised.csv")
  df_ca2 = pd.read_csv("./csvs/new_ca2_revised.csv")
  df_chimei = pd.read_csv("./csvs/chimei_revised.csv")
  df_kenkon = pd.read_csv("./csvs/kenkon_revised.csv")

  # Add new column to dataframe
  df_commonhealth['website'] = 'commonhealth'
  df_nowhealth['website'] = 'nowhealth'
  df_udn['website'] = 'udn'
  df_jah['website'] = 'jah'
  df_ca2['website'] = 'ca2'
  df_chimei['website'] = 'chimei'
  df_kenkon['website'] = 'kenkon'

  # Combined all website csv 
  all_df = pd.concat([df_commonhealth, df_nowhealth, df_udn, df_jah, df_ca2, df_chimei, df_kenkon])


  # Set index on a Dataframe
  all_df.set_index("category", inplace = True)

  # Drop the '外科' category
  all_df.drop(index=['外科'], inplace=True)

  # Output the dataframe to csv
  all_df.to_csv("./../git-repos/all_website_revised.csv")
  all_df

if __name__ == "__main__":
  """ This is executed when run from the command line """
  main()
