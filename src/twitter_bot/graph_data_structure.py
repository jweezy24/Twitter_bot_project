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
    root_node = 'jack_west24'
    nodes = [('NeilKlingensmi4', -130, 0), ('Michael34875097', -29, 143), ('allyssa_fogarty', 244, 183), ('RealCptGonzo', 34, 0), ('alittl3ton13', 6, 0), ('larry_coover', -21, 0), ('christinawest24', 251, 0), ('bennett_west13', 221, 0), ('joe_corno', 129, 0), ('RussianPhilly', -2, 158), ('RishiPatel197', 0, 0), ('a_baig8', -10, 0), ('Qgabs7', 53, 0), ('4steven_', 52, 0), ('alexhunter365', 135, 1), ('lmontrose8', 159, 0), ('sam_elnacho', -31, 0), ('cuffstuff808', 104, 0), ('melissalefko', 21, 0), ('brittanyshea012', -130, 0), ('TGayVanBone', -128, 4), ('businessnplea', -95, 168), ('AshleyLady_', -44, 0), ('culhane_ryan_79', 429, 0), ('MugshotMugs', -105, 0), ('HippyGifs', -91, 2), ('HawkSocks', -82, 0), ('xoxo_itskatie', 76, 0), ('coupe_josh', 23, 0), ('kristendimonda', 17, 0), ('kasey_hendrick', 206, 0), ('Camr0n60', -30, 0), ('Maddie_Werneke', 81, 0), ('Matt_theBrown', -129, 0), ('ReotardL', -80, 2), ('_GabbyCisneros', 120, 0), ('cathynuders', 49, 0), ('ajventrella', 99, 0), ('sam1234556u', -20, 0), ('ManeeshSomisett', 135, 0), ('mitch_west15', 133, 0), ('Saguychenko94', 182, -11), ('Q_Tip_Piper', 176, 0), ('AllyssaFogarty', 58, 0), ('scottwest123', 162, 0), ('CameronnFink', 85, 0), ('sheetsnick', 0, 0), ('madeon', 108, 117), ('michaelreeves', -42, 14), ('Lord_Mandalore', 0, 0), ('Sadieisonfire', -129, -5), ('mach1alex19', 58, 53), ('JacksonATucker', 23, 0), ('jschlatt', -4, 0), ('DONDRRR', 31, 19), ('bbnomula', 19, 44), ('AMDRyzen', 440, 0), ('SuperMegaShow', 52, 77), ('yunggravy', 10, 87), ('zackfox', 3, 4), ('UnusualVideos', -124, 0), ('richbrian', -4, 0), ('nothinbutlag', 54, -2), ('codyko', 54, 310), ('denzelcurry', 258, 160), ('AAAAAGGHHHH', -142, 0), ('LoyolaChicago', 419, 0), ('HugS86', 32, 0), ('Olivertree', 12, 0), ('lildustmop', 5, 89), ('MichaelRCusack', 107, 0), ('aMSaRedyoshi', 203, 118), ('sushitrash', 71, 173), ('TechYESCity', 47, 0), ('nakeyjakey', -9, 75), ('NightmareCops', 75, 0), ('ssbmhax', 69, 0), ('redlettermedia', 163, 117), ('gogreen18', 47, 0), ('GregSalazarYT', 60, 57), ('PostMalone', 171, 779), ('theneedledrop', 109, 0), ('ChrisRGun', -65, 37), ('jacksfilms', 54, 16), ('YungWaff', 264, 243), ('ralphsepe', 54, 193), ('bobbyscar', 188, 137), ('ericandre', -94, 0), ('Panda_Plup', 36, 78), ('OXY_Crimson', 112, 0), ('TempoAxe', 89, 612), ('johnny_S2J', 253, 0), ('TSM_Leffen', 126, 0), ('CLG_PewPewU', 117, 334), ('LiquidHbox', 109, 0), ('C9Mang0', 82, 533), ('PPMD', 149, 0), ('JustinRoiland', 146, 269), ('ArmadaUGS', 127, 0), ('DingDongVG', 49, 0), ('maxmoefoe', -16, 51), ('MVG_Mew2King', 262, 258), ('elirymagee', -23, -10), ('matthwatson', -20, 0), ('boburnham', 86, 0), ('ColossalisCrazy', -24, 40), ('kanyewest', 77, 539), ('anything4views', -28, 90), ('Beetlepimp', 2, 0), ('vgdunkey', -48, 153), ('IHE_OFFICIAL', -51, -7), ('SoBroNo3', 130, 0), ('dylansprouse', 139, 0), ('JonTronShow', -46, 7), ('nikkinacks', -21, 42), ('YtThumbnails', -136, 0), ('RickandMorty', 436, 346), ('Nick_Colletti', 40, 0), ('Idubbbz', 3, 34), ('FilthyFrank', 3, 47), ('RicepirateMick', 41, -6), ('PhillyG811', -3, 62), ('Spazkidin3d', 49, 0), ('NiallerDefiler', 21, 60), ('JohnnyUtahNG', -95, 10), ('LyleRath', 50, 0), ('psychicpebble', 130, 0), ('OneyNG', 131, 79), ('SleepyCabin', 163, -1)]



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