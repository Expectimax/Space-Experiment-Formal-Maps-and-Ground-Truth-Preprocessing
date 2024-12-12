import os
import numpy as np
import osmnx as ox
import networkx as nx
import pandas as pd
import PIL.Image
import tensorflow as tf


# this project is used to create the images for the formal task. In this file you find the utils used in the main file
def create_plots_and_save(polygon, polygon_name, tag_dict, dpi, path_to_save, extension, water_tags):
    # this function is the main function that creates and saves the images in the formal task. The polygon as well as
    # the polygon name come from the shapefile. Additional tags, dpi, the path to save, extensions and water tags can
    # be set
    fp = f'{path_to_save}/{polygon_name}.{extension}'
    # the additional tags to the standard street network that are included in the graph
    useful_tags_way = ox.settings.useful_tags_way + ['railway'] + ['public_transport'] + ['natural']
    ox.settings.useful_tags_way = useful_tags_way
    # create and merge all graphs, the try-except methods are needed since some polygons do not have any street,
    # railway, or waterway networks which would throw an error otherwise
    try:
        # create the street network graph with streets included in the custom filter variable
        G1 = ox.graph_from_polygon(polygon=polygon,
                                   custom_filter='["highway"~"motorway|primary|secondary|tertiary|residential|motorway_link|primary_link|tertiary_link"]',
                                   retain_all=True,
                                   truncate_by_edge=False, simplify=False)
    except ValueError:
        # if there is no street network, return None
        return None

    try:
        # create the rail network graph
        G2 = ox.graph_from_polygon(polygon=polygon, custom_filter='["railway"]', retain_all=True,
                                   truncate_by_edge=False, simplify=False)
        # create the waterway graph
        G3 = ox.graph_from_polygon(polygon=polygon, custom_filter='["natural"~"water"]', retain_all=True,
                                   truncate_by_edge=False, simplify=False)
        # merge the three graphs
        Gf = nx.compose(G1, G2)
        Gf = nx.compose(Gf, G3)
    except ValueError:
        try:
            # create the railway network graph, but not the waterway network
            G2 = ox.graph_from_polygon(polygon=polygon, custom_filter='["railway"]', retain_all=True,
                                       truncate_by_edge=False, simplify=False)
            # merge the two graphs
            Gf = nx.compose(G1, G2)
        except ValueError:
            try:
                # create the waterway network but not the railway network
                G3 = ox.graph_from_polygon(polygon=polygon, custom_filter='["natural"~"water"]', retain_all=True,
                                           truncate_by_edge=False,
                                           simplify=False)
                # merge the two graphs
                Gf = nx.compose(G1, G3)
            except ValueError:
                # if there is no waterway and no railway network, the street network is equal to the final graph
                Gf = G1
    # define the edge colors
    ec = []
    for d in Gf.edges(keys=True, data=True):
        helper_dict = d[3]
        if 'highway' in helper_dict:
            if 'motorway' in helper_dict['highway']:
                ec.append('blue')
            elif 'trunk' in helper_dict['highway']:
                ec.append('gold')
            elif 'primary' in helper_dict['highway']:
                ec.append('gold')
            elif 'secondary' in helper_dict['highway']:
                ec.append('orange')
            elif 'tertiary' in helper_dict['highway']:
                ec.append('orangered')
            elif 'residential' in helper_dict['highway']:
                ec.append('red')
            elif 'unclassified' in helper_dict['highway']:
                ec.append('darkred')
            else:
                ec.append('dimgrey')
        elif 'railway' in helper_dict:
            ec.append('purple')
        elif 'natural' in helper_dict:
            ec.append('deepskyblue')

    # plot the merged graph
    fig, ax = ox.plot_graph(
        G=Gf,
        node_size=0,
        edge_color=ec,
        edge_linewidth=0.15,
        save=False,
        show=False,
        close=True)
    # include the features, i.e. buildings, lakes and so on and colour them. Plot them on top of the existing network
    # plot
    gdf = ox.features_from_polygon(polygon=polygon, tags=tag_dict)
    gdf_water = ox.features_from_polygon(polygon=polygon, tags=water_tags)
    fig, ax = ox.plot_footprints(gdf_water, ax=ax, color='deepskyblue', alpha=0.5, filepath=fp, dpi=dpi, show=True)
    fig, ax = ox.plot_footprints(gdf, ax=ax, color='darkgreen', alpha=0.9, filepath=fp, dpi=dpi, save=True, show=True,
                                 close=True)

    return fig, ax


def create_plots_and_save_landkreis(polygon, polygon_name, tag_dict, dpi, path_to_save, extension, water_tags):
    # this function is basically equivalent to the one before, but it uses the boundaries of a Landkreis instead of
    # a PLZ. This wasn't used in the final version of the work
    fp = f'{path_to_save}/{polygon_name}.{extension}'
    useful_tags_way = ox.settings.useful_tags_way + ['railway'] + ['public_transport'] + ['natural']
    ox.settings.useful_tags_way = useful_tags_way
    G1 = ox.graph_from_polygon(polygon=polygon,
                               custom_filter='["highway"~"motorway|trunk|primary|secondary|tertiary|residential|motorway_link|trunk_link|primary_link|tertiary_link"]',
                               retain_all=True,
                               truncate_by_edge=False, simplify=False)

    street_widths = {"motorway": 0.6, "motorway_link": 0.6, "trunk": 0.4, "trunk_link": 0.4, "primary": 0.3,
                     "primary_link": 0.3, "secondary": 0.2, "secondary_link": 0.2, "tertiary": 0.1,
                     "tertiary_link": 0.1, "residential": 0.1}

    fig, ax = ox.plot_figure_ground(
        G=G1,
        node_size=0,
        color='c',
        street_widths=street_widths,
        default_width=0.15,
        bgcolor='black',
        save=False,
        show=False,
        close=True)

    gdf = ox.features_from_polygon(polygon=polygon, tags=tag_dict)
    gdf_water = ox.features_from_polygon(polygon=polygon, tags=water_tags)
    fig, ax = ox.plot_footprints(gdf_water, ax=ax, color='steelblue', edge_linewidth=0.3, alpha=0.6, filepath=fp,
                                 dpi=dpi, show=True)
    fig, ax = ox.plot_footprints(gdf, ax=ax, color='silver', edge_color='gray', edge_linewidth=0.05, alpha=0.9,
                                 filepath=fp, dpi=dpi, save=True, show=True, )

    return fig, ax


def split_filenames_into_plz(path):
    # this function turns a list of filenames into a list of PLZs
    filenames = os.listdir(path)
    list_of_plz = []
    for file in filenames:
        splitted = file.split('_')
        list_of_plz.append(splitted[0])

    return list_of_plz


def split_filenames_into_ids(path):
    # this function turns a list of filenames into a list of ID's (id of the polygon in the shapefile file)
    filenames = os.listdir(path)
    list_of_ids_long = []
    list_of_ids = []
    for file in filenames:
        splitted = file.split('_')
        list_of_ids_long.append(splitted[3])

    for id_long in list_of_ids_long:
        id = id_long.split('.')
        list_of_ids.append(id[0])

    return list_of_ids


def check_uniqueness_of_plz_in_data(path):
    # this function checks whether each PLZ is unique
    list_of_plz = split_filenames_into_plz(path)
    values1, counts1 = np.unique(list_of_plz, return_counts=True)
    values2, counts2 = np.unique(counts1, return_counts=True)

    if values2 == 1:
        print('All postal codes are unique')
        return True
    else:
        print('There are still non-unique postal codes at the file path')
        return False


def get_non_unique_postal_codes(path):
    # this function returns the PLZs that are not unique
    if check_uniqueness_of_plz_in_data(path):
        print('There are no non unique postal codes')
    else:
        non_unique_plz = []
        list_of_plz = split_filenames_into_plz(path)
        values1, counts1 = np.unique(list_of_plz, return_counts=True)

        for i in range(len(counts1)):
            if counts1[i] != 1:
                non_unique_plz.append(values1[i])

        print(non_unique_plz)
        return non_unique_plz


def check_ground_truth(path, ground_truth):
    # this function checks whether all PLZs that were used to create plots are also included in the ground truth data
    list_of_plz = split_filenames_into_plz(path)
    mismatch_list = []
    for plz in list_of_plz:
        if plz not in ground_truth.index:
            mismatch_list.append(plz)

    for plz in ground_truth.index:
        if plz not in list_of_plz:
            mismatch_list.append(plz)

    if not mismatch_list:
        print('All postal codes in the data and the ground truth match')
        print('Number of instances = ' + str(len(ground_truth)))
    else:
        print('There are postal codes that dont match')
        return mismatch_list


def load_ground_truth(ground_truth_path):
    # this function is used to load the ground truth and splits it into three lists (one for each class)
    population_df = pd.read_excel(ground_truth_path)
    population_df = population_df.drop(['note', 'einwohner', 'qkm', 'lat', 'lon', 'Unnamed: 7', 'Unnamed: 8'],
                                       axis=1).astype(str)

    population_df['plz'] = ['0' + i if len(i) == 4 else i for i in population_df['plz']]
    population_df['Einwohnerdichte'] = [float(i) for i in population_df['Einwohnerdichte']]
    population_df = population_df.sort_values(['Einwohnerdichte'], ascending=False)
    data_list = population_df.values.tolist()

    high_density_list = []
    middle_density_list = []
    low_density_list = []
    for area in data_list:
        if area[1] >= 1250:
            high_density_list.append(area[0])
        elif 1250 > area[1] >= 200:
            middle_density_list.append(area[0])
        elif area[1] < 200:
            low_density_list.append(area[0])
    return high_density_list, middle_density_list, low_density_list


def resize_images(path_to_read, path_to_save, height, width):
    # this function is used to resize the images if necessary
    filenames = os.listdir(path_to_read)

    for file in filenames:
        img = PIL.Image.open(os.path.join(path_to_read, file))
        print(f"Original size: {img.size}")
        img_resized = img.resize((height, width))
        img_resized.save(os.path.join(path_to_save, file))
    print('Resizing and saving the images in a new folder was successful')


def replace_special_characters(path):
    # this function is used to replace any special characters in the filenames
    filenames = os.listdir(path)
    for file in filenames:
        if 'ä' or 'Ä' or 'ü' or 'Ü' or 'ö' or 'Ö' or 'ß' or ' ' in file:
            new_name = file.replace('ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace('ü',
                                                                                                                'ue').replace(
                'Ü', 'Ue').replace('ß', 'ss').replace(' ', '_')

        os.rename(os.path.join(path, file), os.path.join(path, new_name))
    print('Successfully replaced the special characters in the filenames')


def augment_data(path_to_augment, path_augmented, balance):
    # this function is used to create additional images by rotating or flipping them. This is done to get a balanced
    # dataset in the end
    datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=45,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest'
    )

    folder_names = os.listdir(path_to_augment)
    for index, folder in enumerate(folder_names):
        filenames = os.listdir(os.path.join(path_to_augment, folder))
        for filename in filenames:
            file_path = f'{path_to_augment}/{folder}/{filename}'
            img = tf.keras.preprocessing.image.load_img(file_path)
            x = tf.keras.preprocessing.image.img_to_array(img)
            x = x.reshape((1,) + x.shape)
            filename_split = filename.split('.')[0]
            i = 0
            for batch in datagenerator.flow(x, batch_size=1, save_to_dir=f'{path_augmented}/{folder}',
                                            save_prefix=f'{filename_split}_aug',
                                            save_format='png'):
                i += 1
                if i > balance[index]:
                    break


def sort_by_class(path, high_density_list, middle_density_list, low_density_list):
    # this function sorts the images by class and moves them to the respective folder
    filelist = os.listdir(path)
    for file in filelist:
        filepath = os.path.join(path, file)
        plz = file.split('_')[0]
        if plz in high_density_list:
            to_add = 'High'
            new_path = os.path.join(path, to_add)
            new_filepath = os.path.join(new_path, file)
            os.rename(filepath, new_filepath)
        elif plz in middle_density_list:
            to_add = 'Middle'
            new_path = os.path.join(path, to_add)
            new_filepath = os.path.join(new_path, file)
            os.rename(filepath, new_filepath)
        elif plz in low_density_list:
            to_add = 'Low'
            new_path = os.path.join(path, to_add)
            new_filepath = os.path.join(new_path, file)
            os.rename(filepath, new_filepath)
    print("Sorting Images was successful")
