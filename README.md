# ECE1508_Group12Project

## Datasets
**Natural Questions Dataset** Original Repo [Click Here](https://github.com/google-research-datasets/natural-questions)

Kaggle has example preview: https://www.kaggle.com/datasets/validmodel/the-natural-questions-dataset

The original simplified train file (dataset\simplified-nq-train.jsonl) is super large, don't open it. Its first 10000 questions are stored in **dataset\train_file_sample_10000.json**.

Among the 10000, most of the wiki documents only have 1 question, the top-10 wiki documents with most questions have been formatted and stored in **dataset\train_file_sample_selected.json**. `Please use this file for furhter processing!`

> Top 10 document with most questions
> - https://en.wikipedia.org//w/index.php?title=List_of_Super_Bowl_champions&amp;oldid=834538879: 4 questions
> - https://en.wikipedia.org//w/index.php?title=England_at_the_FIFA_World_Cup&amp;oldid=853673134: 4 questions
> - https://en.wikipedia.org//w/index.php?title=Maze_Runner:_The_Death_Cure&amp;oldid=828322653: 3 questions
> - https://en.wikipedia.org//w/index.php?title=England_at_the_FIFA_World_Cup&amp;oldid=856208693: 3 questions
> - https://en.wikipedia.org//w/index.php?title=Cinco_de_Mayo&amp;oldid=842489882: 3 questions
> - https://en.wikipedia.org//w/index.php?title=Great_Pyramid_of_Giza&amp;oldid=800811421: 3 questions
> - https://en.wikipedia.org//w/index.php?title=IPhone_6&amp;oldid=851904769: 3 questions
> - https://en.wikipedia.org//w/index.php?title=History_of_Delhi&amp;oldid=855200091: 3 questions
> - https://en.wikipedia.org//w/index.php?title=Atlanta_Falcons&amp;oldid=833386951: 3 questions
> - https://en.wikipedia.org//w/index.php?title=Abundance_of_elements_in_Earth%27s_crust&amp;oldid=801283417: 3 questions