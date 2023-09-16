// Trait Categories

const difficultyTraits = ["Novice", "Intermediate", "Experienced", "Master", "Grandmaster"];
const releaseDateTraits = ["2001-2007", "2016-2023"];
const seriesTraits = ["Camelot", "Demon Slayer", "Dorgeshuun", "Dragonkin", "Elemental Workshop", "Elf", "Fairytale", "Fremennik", "Gnome", "Great Kourend", "Kharidian", "Mahjarrat", "Miscellania", "Myreque"];
const skillRequirementTraits = ["Attack", "Strength", "Defence", "Ranged", "Prayer", "Magic", "Runecraft", "Hitpoints", "Crafting", "Mining", "Smithing", "Fishing", "Cooking", "Firemaking", "Woodcutting", "Agility", "Herblore", "Thieving", "Fletching", "Slayer", "Farming", "Construction", "Hunter"];
const membershipTraits = ["F2P", "Members"];

// Quest and trait list

let quests = [
    {
        "name": "Animal Magnetism",
        "difficulty": "Intermediate",
        "releaseDate": "2001-2007",
        "skillRequirements": "Slayer Crafting Ranged Woodcutting",
        "membership": "members"
    },
    {
        "name": "Song Of The Elves",
        "difficulty": "Grandmaster",
        "releaseDate": "2001-2007",
        "series": "Elf",
        "skillRequirements": "Agility Construction Farming Herblore Hunter Mining Smithing Woodcutting",
        "membership": "members"
    }
]

console.log(quests[1].skillRequirements.includes("Agility"))
console.log(membershipTraits.length)