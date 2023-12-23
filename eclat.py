import pandas as pd
strong = {}
lift = {}



def sublists(lst, index=0, current=[]):
    if index == len(lst):
        subl.append(frozenset(current))
        return
    sublists(lst, index+1, current)
    sublists(lst, index+1, current + [lst[index]])

def eclat_from_excel(file_path, min_support, min_confidence):
    # Read data from Excel sheet
    df = pd.read_excel(file_path)

    # Assuming the columns are named 'TiD' and 'items'
    # Extract items from the "items" column
    
    #print(dataset)
    eclat_from_dataset(df, min_support, min_confidence)

def eclat_from_dataset(df, min_support, min_confidence):
    # Call the eclat function
    freq_items_eclat = eclat(df, min_support)

    # Print frequent itemsets from Eclat
    print_freq_items_eclat(freq_items_eclat)

    # Represent frequent items as association rules
    association_rules_representation = represent_as_association_rules(freq_items_eclat,min_confidence)
    print_association_rules_representation(association_rules_representation)

    print_strong_rules(strong)

    print_lift(lift)

def eclat(df, min_support):
    items = {}
    #transactions = len(dataset)
    global dataset
    if df.columns[1] == 'items':
        dataset = [list(filter(str.isalpha, str(items))) for items in df['items']]
        global no_rows
        no_rows = len(dataset)
        for i, trans in enumerate(dataset, start=1):
            for item in trans:
                if frozenset({item}) not in items:
                    items[frozenset({item})] = set()
                items[frozenset({item})].add(i)
    else:
        no_rows=0
        for ind in df.index:
            x = str(df['TID_set'][ind]).split(",")
            no_rows = max(int(max(x)),no_rows)
            for id in x:
                if frozenset({df['itemset'][ind]}) not in items:
                    items[frozenset({df['itemset'][ind]})] = set()
                items[frozenset({df['itemset'][ind]})].add(id)


    freq_items = {}
    l = 1
    while l == 1:
        l = 0
        new_items = {}
        for item1 in items:
            if len(items[item1]) >= min_support:
                freq_items[item1] = len(items[item1])

            for item2 in items:
                if item1 != item2:
                    union_set = item1.union(item2)
                    if union_set not in new_items:
                        new_items[union_set] = set(items[item1]).intersection(items[item2])
                        l = 1
        items = new_items

    return freq_items


def represent_as_association_rules(freq_items,min_confidence):
    association_rules_representation = {}

    for itemset, support in freq_items.items():
        if len(itemset) > 1:
            global subl
            subl = []
            sublists(list(itemset))
            for item in subl:
                if len(list(item)) != len(list(itemset)) and len(list(item)) != 0:
                    antecedent = itemset - item
                    consequent = item
                    association_rules_representation[antecedent, consequent] = (support,support/freq_items[antecedent])
                    lift[antecedent, consequent] = (support/no_rows)/((freq_items[antecedent]/no_rows)*(freq_items[consequent]/no_rows))
                    if(min_confidence <= support/freq_items[antecedent]):
                        strong[antecedent, consequent] = support/freq_items[antecedent]
                
    return association_rules_representation

def print_freq_items_eclat(freq_items_eclat):
    print("*************print_freq_items_eclat******************")
    for item, support in freq_items_eclat.items():
        print(f"{list(item)}: {support}")

def print_strong_rules(rules):
    print("*****************************************************")
    print("*************print_strong_rules******************")
    for (antecedent, consequent), (confidence) in rules.items():
        print(f"{list(antecedent)} -> {list(consequent)} : Confidence: {confidence}")

def print_lift(rules):
    print("*****************************************************")
    print("*************print_lift******************")
    for (antecedent, consequent), (lift) in rules.items():
      if lift == 1:
          s="not dependant"
      elif lift>1:
          s="dependant and +VE correlation"
      elif lift<1:
          s="dependant and -VE correlation"    
      print(f"{list(antecedent)} -> {list(consequent)} : lift: {lift}, correlation:{s}")
      

def print_association_rules_representation(rules_representation):
    print("*****************************************************")
    print("*************print_association_rules_representation******************")
    for (antecedent, consequent), (support,conf) in rules_representation.items():
        print(f"{list(antecedent)} -> {list(consequent)} : Support: {support}, Confidence: {conf}")

def main():
    # Example usage with an absolute path using double backslashes
    file_path = r'/content/Virtical_Format.xlsx'
    print("****************************************************************")
    min_support = int(input("Enter a min_support: "))
    min_confidence = float(input("Enter a min_confidence: "))
    print("****************************************************************")
    eclat_from_excel(file_path, min_support, min_confidence)
    print("****************************************************************")

if __name__ == "__main__":
    main()
