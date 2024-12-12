import geopandas as gpd
from utils import create_plots_and_save_landkreis, split_filenames_into_ids, resize_images
# this function wasn't used in the final project. At an earlier time I wanted to create plots of Landkreise instead of
# PLZs, but the number of Landkreise wasn't high enough to get enough images to train a model

multiple_or_single = 0  # create a single plot (=0), or all that are available in the corresponding shape file (=1)
set_plz = 'Kreisfreie Stadt Berlin'  # if single plot is required, set plz to the right location
df = gpd.read_file(
    'C:/Users/ferdi/PycharmProjects/pythonProject8/georef-germany-kreis@public/georef-germany-kreis-millesime.shp')
path = 'C:/Users/ferdi/OneDrive/Desktop'

df.set_geometry('geometry')

tag_dict = {'aeroway': 'aerodrome',
            'public_transport': 'station',
            'amenity': ['university', 'fuel', 'bank', 'hospital'],
            'building': True}
water_tags = {'natural': ['water']}
railway_tags = {'railway': ['light_rail', 'subway', 'tram', 'rail']}


if multiple_or_single == 0:
    index = [155]
    for i in index:
        polygon_name = 'Muenchen'
        print(polygon_name)
        polygon = df['geometry'].iloc[i]
        create_plots_and_save_landkreis(polygon, polygon_name, tag_dict,
                                        dpi=2000,
                                        path_to_save=path,
                                        extension='png',
                                        water_tags=water_tags,
                                        )

elif multiple_or_single == 1:
    plz = df['name']
    name = df['plz_name']
    lan_name = df['lan_name']
    id_list = split_filenames_into_ids(path)

    for i in range(df.shape[0]):
        if i in id_list:
            polygon = df['geometry'].iloc[i]
            polygon_name = plz[i] + '_' + name[i] + '_' + lan_name[i] + '_' + str(i)
            print(polygon_name)
            create_plots_and_save_landkreis(polygon, polygon_name, tag_dict, dpi=2000, path_to_save=path,
                                            extension='png')
