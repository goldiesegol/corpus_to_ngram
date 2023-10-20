from shiny import App, ui,reactive, render
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def relfreq(age,pattern,df):
    age_subset = df[df.age==age]
    len_subset = age_subset[age_subset.length==len(pattern)]
    if(len(len_subset)>0):
        pattern_subset = len_subset[len_subset.ngram==pattern]
        return pattern_subset.size/len_subset.size
    else: return 0

def relfreq_pos(age,pattern,df):
    age_subset = df[df.age==age]
    len_subset = age_subset[age_subset.length==len(pattern.split(' '))]
    if(len(len_subset)>0):
        pattern_subset = len_subset[len_subset.ngram==pattern]
        return pattern_subset.size/len_subset.size
    else: return 0

def relfreq_df(df):
    RESULT_COL = ['ngram','age','relative frequency']
    result = pd.DataFrame(columns = RESULT_COL)
    for gram in df.ngram.unique():
        for AGE in df.age.unique():
            result.loc[len(result.index)] = [gram,AGE,(relfreq(AGE,gram,df))]
    return result

def relfreq_df_pos(df):
    RESULT_COL = ['ngram','age','relative frequency']
    result = pd.DataFrame(columns = RESULT_COL)
    for gram in df.ngram.unique():
        for AGE in df.age.unique():
            result.loc[len(result.index)] = [gram,AGE,(relfreq_pos(AGE,gram,df))]
    return result


def get_graph(df,gram):
    subset = df[df.ngram==gram]
    return sns.lmplot(data=subset, x="age", y="relative frequency").set(title=gram)
    #plt.show()

def get_graphs(df,ngram_list):
    n = len(ngram_list)

    if(n>1):

        fig, axs = plt.subplots(ncols=n)

        for i in range(0,n):
            sns.regplot(df[df.ngram==ngram_list[i]],x='age',y='relative frequency',ax=axs[i]).set(title=ngram_list[i])
        return fig
    else: return(get_graph(df,ngram_list[0]))

def unique_list_nlen(l,n,mode):

    if(mode=='pos'): result = [item for item in l if len(item.split(' '))==n]
    elif(mode == 'pat'): result = [item for item in l if len(item)==n]
    return result

pat = pd.read_csv('PAT.csv')
pos = pd.read_csv('POS.csv')





types = ['POS','Pattern']

pos_unique = list(pos.ngram.unique())
pat_unique = list(pat.ngram.unique())

pat_rel_freq = relfreq_df(pat)
pos_rel_freq = relfreq_df_pos(pos)



# Part 1: ui ----
app_ui = ui.page_fluid(
    ui.navset_tab_card(
        ui.nav("process csv",
            ui.input_radio_buttons("csv_bool", "Do you already have a CSV file with POS and PAT ngrams?", ['yes','no']),
            ui.panel_conditional(
                "input.csv_bool=='yes'",
                ui.input_text("POS_csv", "Input POS csv file", placeholder="POS.csv"),
                ui.input_text("PAT_csv", "Input PAT csv file", placeholder="PAT.csv"),
                ui.p(ui.input_action_button("process_both_csvs", "Go!")),
            ),
            ui.panel_conditional(
                "input.csv_bool=='no'",
                ui.input_text("orig_csv", "Input PAT csv file", placeholder="PAT.csv"),
                ui.p(ui.input_action_button("process_orig_csv", "Go!")),
            )


        ),
        ui.nav("config",
            ui.input_selectize("type", "Type",types),
            ui.input_slider("comp_len", "How many graphs would you like to see?",value=1,min=1,max=3),
            ui.input_slider("ngram_len", "Select ngram length",value=2,min=2,max=4)
            #ui.input_selectize("reduce","Limit selection to these components",value=)
        ),

        # INPUT TAG DECODER
        # SELECT_NNN
        # N1 = N GRAPHS
        # N2 = NGRAM LENGTH
        # N3 = N SELECTION
        ui.nav("graphs",
            ui.panel_conditional(
                "input.type=='POS'",

                #1 graph
                ui.panel_conditional(
                    "input.comp_len==1",

                    #2-gram
                    ui.panel_conditional(
                        "input.ngram_len==2",
                        ui.input_selectize("pos_select_121","Select ngram",unique_list_nlen(pos_unique,2,'pos'))
                    ),

                    #3-gram
                    ui.panel_conditional(
                        "input.ngram_len==3",
                        ui.input_selectize("pos_select_131","Select ngram",unique_list_nlen(pos_unique,3,'pos'))
                    ),

                    #4-gram
                    ui.panel_conditional(
                        "input.ngram_len==4",
                        ui.input_selectize("pos_select_141","Select ngram",unique_list_nlen(pos_unique,4,'pos'))
                    )
                ),


                # 2 graphs
                ui.panel_conditional(
                    "input.comp_len==2",
                    #2-gram
                    ui.panel_conditional(
                        "input.ngram_len==2",
                        ui.input_selectize("pos_select_221","Select ngram",unique_list_nlen(pos_unique,2,'pos')),
                        ui.input_selectize("pos_select_222","Select ngram",unique_list_nlen(pos_unique,2,'pos'))
                    ),

                    #3-gram
                    ui.panel_conditional(
                        "input.ngram_len==3",
                        ui.input_selectize("pos_select_231","Select ngram",unique_list_nlen(pos_unique,3,'pos')),
                        ui.input_selectize("pos_select_232","Select ngram",unique_list_nlen(pos_unique,3,'pos'))
                    ),

                    #4-gram
                    ui.panel_conditional(
                        "input.ngram_len==4",
                        ui.input_selectize("pos_select_241","Select ngram",unique_list_nlen(pos_unique,4,'pos')),
                        ui.input_selectize("pos_select_242","Select ngram",unique_list_nlen(pos_unique,4,'pos'))
                    )
                ),


                # 3 graphs
                ui.panel_conditional(
                    "input.comp_len==3",
                    #2-gram
                    ui.panel_conditional(
                        "input.ngram_len==2",
                        ui.input_selectize("pos_select_321","Select ngram",unique_list_nlen(pos_unique,2,'pos')),
                        ui.input_selectize("pos_select_322","Select ngram",unique_list_nlen(pos_unique,2,'pos')),
                        ui.input_selectize("pos_select_323","Select ngram",unique_list_nlen(pos_unique,2,'pos'))
                    ),

                    #3-gram
                    ui.panel_conditional(
                        "input.ngram_len==3",
                        ui.input_selectize("pos_select_331","Select ngram",unique_list_nlen(pos_unique,3,'pos')),
                        ui.input_selectize("pos_select_332","Select ngram",unique_list_nlen(pos_unique,3,'pos')),
                        ui.input_selectize("pos_select_333","Select ngram",unique_list_nlen(pos_unique,3,'pos'))



                    ),

                    #4-gram
                    ui.panel_conditional(
                        "input.ngram_len==4",
                        ui.input_selectize("pos_select_431","Select ngram",unique_list_nlen(pos_unique,4,'pos')),
                        ui.input_selectize("pos_select_432","Select ngram",unique_list_nlen(pos_unique,4,'pos')),
                        ui.input_selectize("pos_select_433","Select ngram",unique_list_nlen(pos_unique,4,'pos'))
                    )
                )


            ),
            ui.panel_conditional(
                      "input.type=='Pattern'",

                      #1 graph
                      ui.panel_conditional(
                          "input.comp_len==1",

                          #2-gram
                          ui.panel_conditional(
                              "input.ngram_len==2",
                              ui.input_selectize("pat_select_121","Select ngram",unique_list_nlen(pat_unique,2,'pat'))

                          ),

                          #3-gram
                          ui.panel_conditional(
                              "input.ngram_len==3",
                              ui.input_selectize("pat_select_131","Select ngram",unique_list_nlen(pat_unique,3,'pat'))
                          ),

                          #4-gram
                          ui.panel_conditional(
                              "input.ngram_len==4",
                              ui.input_selectize("pat_select_141","Select ngram",unique_list_nlen(pat_unique,4,'pat'))
                          )
                      ),


                      # 2 graphs
                      ui.panel_conditional(
                          "input.comp_len==2",
                          #2-gram
                          ui.panel_conditional(
                              "input.ngram_len==2",
                              ui.input_selectize("pat_select_221","Select ngram",unique_list_nlen(pat_unique,2,'pat')),
                              ui.input_selectize("pat_select_222","Select ngram",unique_list_nlen(pat_unique,2,'pat'))
                          ),

                          #3-gram
                          ui.panel_conditional(
                              "input.ngram_len==3",
                              ui.input_selectize("pat_select_231","Select ngram",unique_list_nlen(pat_unique,3,'pat')),
                              ui.input_selectize("pat_select_232","Select ngram",unique_list_nlen(pat_unique,3,'pat'))
                          ),

                          #4-gram
                          ui.panel_conditional(
                              "input.ngram_len==4",
                              ui.input_selectize("pat_select_241","Select ngram",unique_list_nlen(pat_unique,4,'pat')),
                              ui.input_selectize("pat_select_242","Select ngram",unique_list_nlen(pat_unique,4,'pat'))
                          )
                      ),


                      # 3 graphs
                      ui.panel_conditional(
                          "input.comp_len==3",
                          #2-gram
                          ui.panel_conditional(
                              "input.ngram_len==2",
                              ui.input_selectize("pat_select_321","Select ngram",unique_list_nlen(pat_unique,2,'pat')),
                              ui.input_selectize("pat_select_322","Select ngram",unique_list_nlen(pat_unique,2,'pat')),
                              ui.input_selectize("pat_select_323","Select ngram",unique_list_nlen(pat_unique,2,'pat'))
                          ),

                          #3-gram
                          ui.panel_conditional(
                              "input.ngram_len==3",
                              ui.input_selectize("pat_select_331","Select ngram",unique_list_nlen(pat_unique,3,'pat')),
                              ui.input_selectize("pat_select_332","Select ngram",unique_list_nlen(pat_unique,3,'pat')),
                              ui.input_selectize("pat_select_333","Select ngram",unique_list_nlen(pat_unique,3,'pat'))



                          ),

                          #4-gram
                          ui.panel_conditional(
                              "input.ngram_len==4",
                              ui.input_selectize("pat_select_431","Select ngram",unique_list_nlen(pat_unique,4,'pat')),
                              ui.input_selectize("pat_select_432","Select ngram",unique_list_nlen(pat_unique,4,'pat')),
                              ui.input_selectize("pat_select_433","Select ngram",unique_list_nlen(pat_unique,4,'pat'))
                          )
                      )


                  ),
                  ui.output_plot("to_plot"),
        )





        )

        )



# Part 2: server ----
def server(input, output, session):
    @output
    @render.plot



    def to_plot():
        if(input.type()=='POS'):
            df = pos_rel_freq
            if(input.comp_len()==1):
                if(input.ngram_len()==2): ngram_list=[str(input.pos_select_121())]
                elif(input.ngram_len()==3): ngram_list=[str(input.pos_select_131())]
                elif(input.ngram_len()==4): ngram_list=[str(input.pos_select_141())]
            elif(input.comp_len()==2):
                if(input.ngram_len()==2): ngram_list=[str(input.pos_select_221()),str(input.pos_select_222())]
                elif(input.ngram_len()==3): ngram_list=[str(input.pos_select_231()),str(input.pos_select_232())]
                elif(input.ngram_len()==4): ngram_lis=[str(input.pos_select_241()),str(input.pos_select_242())]
            elif(input.comp_len()==3):
                if(input.ngram_len()==2): ngram_list=[str(input.pos_select_321()),str(input.pos_select_322()),str(input.pos_select_323())]
                elif(input.ngram_len()==3): ngram_list=[str(input.pos_select_331()),str(input.pos_select_332()),str(input.pos_select_333())]
                elif(input.ngram_len()==4): ngram_lis=[str(input.pos_select_341()),str(input.pos_select_342()),str(input.pos_select_343())]

        elif(input.type()=='Pattern'):
            df = pat_rel_freq
            if(input.comp_len()==1):
                if(input.ngram_len()==2): ngram_list=[str(input.pat_select_121())]
                elif(input.ngram_len()==3): ngram_list=[str(input.pat_select_131())]
                elif(input.ngram_len()==4): ngram_list=[str(input.pat_select_141())]
            elif(input.comp_len()==2):
                if(input.ngram_len()==2): ngram_list=[str(input.pat_select_221()),str(input.pat_select_222())]
                elif(input.ngram_len()==3): ngram_list=[str(input.pat_select_231()),str(input.pat_select_232())]
                elif(input.ngram_len()==4): ngram_lis=[str(input.pat_select_241()),str(input.pat_select_242())]
            elif(input.comp_len()==3):
                if(input.ngram_len()==2): ngram_list=[str(input.pat_select_321()),str(input.pat_select_322()),str(input.pat_select_323())]
                elif(input.ngram_len()==3): ngram_list=[str(input.pat_select_331()),str(input.pat_select_332()),str(input.pat_select_333())]
                elif(input.ngram_len()==4): ngram_lis=[str(input.pat_select_341()),str(input.pat_select_342()),str(input.pat_select_343())]

        return get_graphs(df,ngram_list)


app = App(app_ui, server)
