const quests = [
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
    // Add more quests as needed
];

// Extract possible trait values from quests
const possibleTraits = {
    difficulty: [...new Set(quests.map(q => q.difficulty))],
    releaseDate: [...new Set(quests.map(q => q.releaseDate))],
    series: [...new Set(quests.filter(q => q.series).map(q => q.series))],
    membership: [...new Set(quests.map(q => q.membership))],
    skillRequirements: [...new Set(quests.flatMap(q => q.skillRequirements.split(' ')))]
};

// Assign unique traits to A1, A2, A3 and B1, B2, B3 for non-reusable traits
const A_traits = {
    A1: getRandomItem(possibleTraits.difficulty),
    A2: getRandomItem(possibleTraits.releaseDate),
    A3: getRandomItem(possibleTraits.series)
};

const B_traits = {
    B1: getRandomItem(possibleTraits.skillRequirements),
    B2: getRandomItem(possibleTraits.skillRequirements),
    B3: getRandomItem(possibleTraits.membership)
};

// Ensure that the combination of A and B traits matches at least one quest
const gridAssignments = {};
['A1', 'A2', 'A3'].forEach(aKey => {
    ['B1', 'B2', 'B3'].forEach(bKey => {
        const aTrait = A_traits[aKey];
        const bTrait = B_traits[bKey];

        // Check if the combination of A and B exists in at least one quest
        const validQuest = quests.find(q =>
            (q.difficulty === aTrait || q.releaseDate === aTrait || q.series === aTrait) &&
            (q.skillRequirements.split(' ').includes(bTrait) || q.membership === bTrait)
        );

        if (validQuest) {
            gridAssignments[`${aKey}-${bKey}`] = {
                aTrait: aTrait,
                bTrait: bTrait
            };
        } else {
            // Reassign a new trait if the combination isn't valid
            gridAssignments[`${aKey}-${bKey}`] = {
                aTrait: getRandomItem(possibleTraits.difficulty),
                bTrait: getRandomItem(possibleTraits.skillRequirements)
            };
        }
    });
});

// Add event listeners to grid buttons
document.querySelectorAll('.grid-item').forEach(item => {
    item.addEventListener('click', () => {
        const gridKey = item.id;
        const assignment = gridAssignments[gridKey];

        // Provide the A and B traits as a hint to the user
        const hint = `Trait 1 (A): ${assignment.aTrait}\nTrait 2 (B): ${assignment.bTrait}`;

        const userGuess = prompt(`Guess the quest associated with ${gridKey}:\n${hint}`);

        // Check if the guess is correct by comparing it to the quests
        const correctQuest = quests.find(q =>
            (q.difficulty === assignment.aTrait || q.releaseDate === assignment.aTrait || q.series === assignment.aTrait) &&
            (q.skillRequirements.split(' ').includes(assignment.bTrait) || q.membership === assignment.bTrait)
        );

        if (userGuess && correctQuest && userGuess.toLowerCase() === correctQuest.name.toLowerCase()) {
            alert(`Correct! The quest is "${correctQuest.name}".`);
        } else {
            alert(`Wrong! The correct quest was "${correctQuest ? correctQuest.name : 'No matching quest found'}".`);
        }
        
    });
});

console.log(gridAssignments);

// Utility function to get a random item from an array
function getRandomItem(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}
