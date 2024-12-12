import geopandas as gpd
from utils import create_plots_and_save, split_filenames_into_ids, resize_images

# this file is used to create the images for the PLZs. You can decide whether you want one create one single PLZ or all
# that are available by setting the "multiple or single" variable

multiple_or_single = 1  # create a single plot (=0), or all that are available in the corresponding shape file (=1)
set_plz = '81375'  # if single plot is required, set plz to the right location
df = gpd.read_file('C:/Users/ferdi/PycharmProjects/pythonProject8/'
                   'georef-germany-postleitzahl@public/georef-germany-postleitzahl.shp')
path = 'C:/Users/ferdi/OneDrive/Masterarbeit/Datasets/Maps'

df.set_geometry('geometry')

tag_dict = {'highway': True,
            'aeroway': 'aerodrome',
            'railway': ['rail', 'light_rail', 'subway', 'tram'],
            'public_transport': 'station',
            'amenity': ['university', 'fuel', 'parking', 'bank', 'hospital'],
            'building': True}

if multiple_or_single == 0:
    index = df.name[df.name == set_plz].index
    name = df['plz_name']
    lan_name = df['lan_name']
    for i in index:
        polygon_name = set_plz + '_' + name[i] + '_' + lan_name[i] + '_' + str(i)
        print(polygon_name)
        polygon = df['geometry'].iloc[i]
        create_plots_and_save(polygon, polygon_name, tag_dict, dpi=150, path_to_save=path, extension='png')

elif multiple_or_single == 1:
    index_list = list(df['name'].index)
    plz = df['name']
    name = df['plz_name']
    lan_name = df['lan_name']

    for i in range(df.shape[0]):
        if i in index_list:
            polygon = df['geometry'].iloc[i]
            polygon_name = plz[i] + '_' + name[i] + '_' + lan_name[i] + '_' + str(i)
            print(polygon_name)
            create_plots_and_save(polygon, polygon_name, tag_dict, dpi=150, path_to_save=path, extension='png')
