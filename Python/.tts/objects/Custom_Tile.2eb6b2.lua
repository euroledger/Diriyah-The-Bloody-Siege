deckGUID = "386d00"

function onLoad()
self.setLock(true)
createButtons()
end

function createButtons()


self.clearButtons()

self.createButton({
    label="Draw",
    click_function="drawCard",
    function_owner=self,
    position={0,0.6,0.5},
    rotation={0,,0},
    width=1200,
    height=500,
    font_size=250
})

self.createButton({
    label="Shuffle",
    click_function="shuffleDeck",
    function_owner=self,
    position={0,0.6,-0.5},
    rotation={0,180,0},
    width=1200,
    height=500,
    font_size=250
})


end

function getDeck()
return getObjectFromGUID(deckGUID)
end

function drawCard()


local deck = getDeck()
if not deck then return end

local pos = self.getPosition() + Vector(10,2,0)

if deck.tag == "Deck" then

    deck.takeObject({
        position = pos,
        rotation = {0,180,0}
    })

elseif deck.tag == "Card" then

    deck.setPositionSmooth(pos)
    deck.setRotationSmooth({0,180,0})

end


end

function shuffleDeck()


local deck = getDeck()

if deck and deck.tag == "Deck" then
    deck.shuffle()
end


end
