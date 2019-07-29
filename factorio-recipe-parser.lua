data = {}
data["extend"] = function (data, t)
    for n, recipe in ipairs(t) do
        if (recipe["ingredients"] == nil) then
            ing = recipe["normal"]["ingredients"]
        else
            ing = recipe["ingredients"]
        end
        print(recipe["name"] .. ":")
        for i, component in ipairs(ing) do
            cname = component[1] or component["name"]
            camt = component[2] or component["amount"]
            print("    - " .. cname )
        end
    end
end

files = {
    "ammo",
    "capsule",
    "demo-furnace-recipe",
    "demo-recipe",
    "demo-turret",
    "equipment",
    "fluid-recipe",
    "furnace-recipe",
    "inserter",
    "module",
    "recipe",
    "turret",
}

for i, f in ipairs(files) do
    dofile("D:\\Games\\Steam\\SteamApps\\common\\Factorio\\data\\base\\prototypes\\recipe\\" .. f .. ".lua")
end
