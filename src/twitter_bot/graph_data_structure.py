import networkx as nx
import matplotlib.pyplot as plt

''' 
This method will create a graph object for the visualization.
input:
    list of nodes with distances
output:
    graph object with the nodes with their distances.
'''
def create_graph_obj_test():
    # root_node = 'jack_west24'
    # nodes = [('NeilKlingensmi4', -62, -38), ('Michael34875097', -55, -38), ('allyssa_fogarty', -65, -35), ('RussianPhilly', -28, -10), ('christinawest24', 247, -25), ('alittl3ton13', 123, -34), ('alexhunter365', 124, -38), ('melissalefko', 188, -2), ('bennett_west13', 279, 7), ('RishiPatel197', 109, -9), ('joe_corno', 268, 17), ('cuffstuff808', 47, 7), ('brittanyshea012', -59, -36), ('TGayVanBone', -69, -38), ('businessnplea', -52, -24), ('4steven_', 56, -31), ('AshleyLady_', 217, 1), ('lmontrose8', 202, 19), ('MugshotMugs', -38, -38), ('HippyGifs', -22, -34), ('HawkSocks', -48, -38), ('kasey_hendrick', 294, 0), ('culhane_ryan_79', 297, -38), ('xoxo_itskatie', 94, -20), ('ReotardL', -8, -38), ('kristendimonda', 169, -38), ('sam1234556u', 69, -38), ('Maddie_Werneke', 240, 26), ('Camr0n60', 96, -38), ('coupe_josh', 57, -14), ('Matt_theBrown', -62, -38), ('cathynuders', -65, -24), ('_GabbyCisneros', 70, -38), ('ManeeshSomisett', 248, 55), ('ajventrella', 194, 63), ('mitch_west15', 226, 28), ('scottwest123', 146, 30), ('AllyssaFogarty', 97, -36), ('Q_Tip_Piper', 332, -6), ('CameronnFink', 206, 0), ('sheetsnick', 109, -2), ('madeon', 230, -38), ('jschlatt', 127, -38), ('michaelreeves', 9, -12), ('mach1alex19', 158, 11), ('Lord_Mandalore', 101, -31), ('AMDRyzen', 847, -4), ('Sadieisonfire', -51, -39), ('DONDRRR', 116, -33), ('richbrian', 99, -38), ('bbnomula', 77, -26), ('JacksonATucker', 139, -38), ('yunggravy', 142, -5), ('codyko', 154, 30), ('nothinbutlag', 167, -22), ('denzelcurry', 390, -38), ('UnusualVideos', -55, -35), ('zackfox', 67, -135), ('SuperMegaShow', 222, 4), ('AAAAAGGHHHH', -73, -36), ('Olivertree', 78, -25), ('MichaelRCusack', 211, 33), ('lildustmop', 89, -38), ('LoyolaChicago', 667, -31), ('HugS86', 358, -38), ('ssbmhax', 169, -10), ('sushitrash', 163, -38), ('NightmareCops', 172, -38), ('redlettermedia', 202, -38), ('nakeyjakey', 115, -27), ('aMSaRedyoshi', 559, -29), ('TechYESCity', 161, -34), ('GregSalazarYT', 286, -11), ('PostMalone', 237, -38), ('gogreen18', 193, -33), ('YungWaff', 497, 196), ('theneedledrop', 281, -1), ('bobbyscar', 331, 28), ('jacksfilms', 262, -37), ('OXY_Crimson', 260, -38), ('Panda_Plup', 132, -12), ('ChrisRGun', 5, -34), ('ericandre', 40, 34), ('TempoAxe', 200, 73), ('PPMD', 270, 62), ('ralphsepe', 122, -38), ('JustinRoiland', 222, -38), ('CLG_PewPewU', 337, -38), ('johnny_S2J', 399, 244), ('LiquidHbox', 241, -38), ('TSM_Leffen', 410, 283), ('elirymagee', 107, -30), ('C9Mang0', 150, 216), ('ArmadaUGS', 254, -38), ('MVG_Mew2King', 745, -23), ('maxmoefoe', 65, -16), ('ColossalisCrazy', 60, -38), ('anything4views', 57, -38), ('boburnham', 240, -38), ('DingDongVG', 149, -25), ('matthwatson', 90, -38), ('kanyewest', 191, -38), ('Beetlepimp', 76, -38), ('SoBroNo3', 160, -38), ('IHE_OFFICIAL', 42, -38), ('vgdunkey', 35, -13), ('dylansprouse', 234, -38), ('Nick_Colletti', 77, -38), ('nikkinacks', 61, -20), ('Idubbbz', 102, -38), ('YtThumbnails', -72, -38), ('RickandMorty', 421, -38), ('JonTronShow', 43, -38), ('FilthyFrank', -71, -36), ('RicepirateMick', 154, -27), ('LyleRath', 128, -38), ('Spazkidin3d', 124, -38), ('PhillyG811', 62, -38), ('NiallerDefiler', 110, -38), ('JohnnyUtahNG', -9, -38), ('psychicpebble', 192, -38), ('OneyNG', 214, -38), ('SleepyCabin', 217, -35)]


    # G = nx.Graph()
    # G.add_node(root_node)

    # for node,x,y in nodes:
    #     G.add_node(node)
    #     print(f"{x} {y} {node}")
    #     G.add_edge(root_node, node, weight=(y/x))
    
    plt.annotate(xy=[0,0], s=root_node)
    for node,x,y in nodes:
        plt.annotate(xy=[x,y], s=node)
        plt.plot([0,x], [0,y])

    #nx.draw(G, with_labels=True)
    plt.show()


if __name__ == "__main__":
    create_graph_obj_test()