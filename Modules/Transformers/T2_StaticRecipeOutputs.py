
def T2_StaticRecipeOutputs(recipes):

    outputs = {} # key is output, list item 0 is all recipes, list item 1 is all inputs for every recipe
    
    for recipe in recipes.keys():
        key = recipes[recipe]['Outputs'][0]['Ticker']
        if key not in outputs.keys():
            outputs[key] = [[],[]]
        outputs[key][0].append(recipe)
        input_list = []
        for input in recipes[recipe]['Inputs']:
            input_list.append(input['Ticker'])
        for item in input_list:
            if item not in outputs[key][1]:
                outputs[key][1].append(item)

    outputs['NA'] = [['=>NA'],[]]
    
    return outputs
    