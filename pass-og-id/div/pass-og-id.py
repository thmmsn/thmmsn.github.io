import json
import requests
import time
import os
from datetime import datetime, timedelta


# PASS
PublicId = 'd1b043c75655a6756852ba9892255243c08688a071e3b58b64c892524f58d098'
# ID-KORT
#PublicId = '8e859bd4c1752249665bf2363ea231e1678dbb7fc4decff862d9d41975a9a95a'

begynn_link = "https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branches/"
slutt_link =";service" + "PublicId=" + PublicId + ";customSlotLength=10"

branch_grupper = requests.get("https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branchGroups/"+slutt_link)
branch_grupper = branch_grupper.json()

# minimaliser
branch_grupper = branch_grupper[:2]

# Liste over alle politidistrikter
politidistrikt = []
for distrikter in branch_grupper:
    politidistrikt.append({'distrikt' : distrikter['name']})
# Liste over alle politistasjoner
politistasjon = []
for distrikter in branch_grupper:
    for branch in distrikter['branches']:
            politistasjon.append({'politistasjoner' : branch['name']})

# Definere funksjoner

def politi_alle_distrikt(d):
    antall_dager = datetime.today() + timedelta(d)
    for distrikter in branch_grupper:
        #print('')
        print(distrikter['name'])
        print("------------------------------------")
        for branch in distrikter['branches']:
            print("\t",branch['name'])

def politi_sted(branchname, d):
    antall_dager = datetime.today() + timedelta(d)
    for distrikter in branch_grupper:
        for branch in distrikter['branches']:
            if branch['name'] == branchname:
                ledige_datoer = requests.get(begynn_link + branch['id'] + "/dates" + slutt_link)
                ledige_datoer = ledige_datoer.json()
                print(branch['name'])
                print("------------------------------------")
                for datoer in ledige_datoer:
                    if datetime.strptime(datoer['date'], '%Y-%m-%d') <= antall_dager:
                        ledige_datoer_og_klokkeslett = requests.get(begynn_link + branch['id'] + '/dates/' + datoer['date'] + '/times' + slutt_link)
                        ledige_datoer_og_klokkeslett = ledige_datoer_og_klokkeslett.json()
                        # print("\t\t",dates['date'])
                        print('\t\t',datoer['date'])
                        for klokkeslett in ledige_datoer_og_klokkeslett:
                            print('\t\t\t', klokkeslett['time'])

def politi_distrikt(distriktnavn, d):
    antall_dager = datetime.today() + timedelta(d)
    for distrikter in branch_grupper:
        if distrikter['name'] == distriktnavn:
            #print('')
            print(distrikter['name'])
            for branch in distrikter['branches']:
                ledige_datoer = requests.get(begynn_link + branch['id'] + "/dates" + slutt_link)
                ledige_datoer = ledige_datoer.json()
                print("\t",branch['name'])
                for datoer in ledige_datoer:
                    if datetime.strptime(datoer['date'], '%Y-%m-%d') <= antall_dager:
                        ledige_datoer_og_klokkeslett = requests.get(begynn_link + branch['id'] + '/dates/' + datoer['date'] + '/times' + slutt_link)
                        ledige_datoer_og_klokkeslett = ledige_datoer_og_klokkeslett.json()
                        # print("\t\t",dates['date'])
                        print('\t\t',datoer['date'])
                        for klokkeslett in ledige_datoer_og_klokkeslett:
                            print('\t\t\t', klokkeslett['time'])

def politi_distrikt_json(d):
    file = open('data.json', 'w')
    antall_dager = datetime.today() + timedelta(d)

    file.write('{ "data" : {\n')

    print('{ "data" : {')

    m = 1
    for distrikter in branch_grupper:
    #if distrikter['name'] == distriktnavn:
        # Trøndelag politidistrikt
        antall_distrikter_in_branch_grupper = len(branch_grupper)

        file.write('\t"' + distrikter['name'] +'" : {\n')
        
        print('\t"',distrikter['name'],'" : {')
        l = 1
        for politistasjon in distrikter['branches']:

            antall_politistasjon_in_distrikter = len(distrikter['branches'])
            ledige_datoer = requests.get(begynn_link + politistasjon['id'] + "/dates" + slutt_link)
            ledige_datoer = ledige_datoer.json()

            antall_ledige_datoer = 0
            d = []
            for i in ledige_datoer:
                if datetime.strptime(i['date'], '%Y-%m-%d') <= antall_dager:
                    d.append(i)
                    antall_ledige_datoer = antall_ledige_datoer + 1
            ledige_datoer = d

            file.write('\t\t"' + politistasjon['name'] + '" : [{\n')
            
            print('\t\t"',  politistasjon['name'],  '" : [{')

            k = 1
            for datoer in ledige_datoer:
                ledige_datoer_og_klokkeslett = requests.get(begynn_link + politistasjon['id'] + '/dates/' + datoer['date'] + '/times' + slutt_link)
                ledige_datoer_og_klokkeslett = ledige_datoer_og_klokkeslett.json()

                file.write('\t\t\t"'+datoer['date']+'":[\n')

                print('\t\t\t"',datoer['date'],'":[')
                
                j = 1
                for klokkeslett in ledige_datoer_og_klokkeslett:
                    antall_ledige_klokkeslett = len(ledige_datoer_og_klokkeslett)
                    # "12:05"
                    if j < antall_ledige_klokkeslett:

                        file.write('\t\t\t\t"'+klokkeslett['time']+'",\n')
                        
                        print('\t\t\t\t"',klokkeslett['time'],'",')
                    if j == antall_ledige_klokkeslett:

                        file.write('\t\t\t\t"'+klokkeslett['time']+'"\n')
                        
                        print('\t\t\t\t"',klokkeslett['time'],'"')
                    j = j+1
                if k < antall_ledige_datoer:
                    file.write('\t\t\t],\n')
                    print('\t\t\t],')
                if k == antall_ledige_datoer:
                    file.write('\t\t\t]\n')
                    print('\t\t\t]')
                k = k+1

            if l < antall_politistasjon_in_distrikter:
                file.write('\t\t}],\n')
                print('\t\t}],')
            if l == antall_politistasjon_in_distrikter:
                file.write('\t\t}]\n')
                print('\t\t}]')
            l = l+1
        # OK
        if m < antall_distrikter_in_branch_grupper:
            file.write('\t},\n')
            print('\t},\n')
        if m == antall_distrikter_in_branch_grupper:
            file.write('\t}\n')
            print('\t}\n')
        m = m+1
    file.write("}\n}\n")
    print("}\n}\n")
    file.close()


#start_time = time.time()
#politi_alle_distrikt(7)
#print("--- %s seconds ---" % (time.time() - start_time))

# funksjonen for distrikt kan generere html for nettside
# pass-og-id.no/trondelag/heimdal/?d=7
# /more-og-romsdal/alesund

# start_time = time.time()
politi_distrikt_json(14)
# print("--- %s seconds ---" % (time.time() - start_time))



# politi_alle_distrikt_json(7)

#politi_sted('Heimdal politistasjon',14)
#print("--- %s seconds ---" % (time.time() - start_time))
# print(politidistrikt)









