
flat_iter = []
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
lo_query_links = natsorted(glob.glob(str(os.getcwd())+'*.csv'))
list_per_links = []
for p,fileName in enumerate(lo_query_links):
    b = os.path.getsize(fileName)
    if b>250: # this is just to prevent reading in of incomplete data.
        file_contents = pd.read_csv(fileName)
        for index in range(0,len(file_contents)):
            flat_iter.append((p,fileName,file_contents,index))
print(flat_iter)

import dask.bag as db
grid = db.from_sequence(flat_iter)
urlDats = list(db.map(web_iter,grid).compute())

if frames ==True:
    unravel = process_dics(urlDats)
else:
    unravel = urlDats

with open('unraveled_links.p','wb') as handle:
    pickle.dump(unravel,handle)
