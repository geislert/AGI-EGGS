-- EchoSeed HALO Language Learning Agent (simplified)
-- Demonstrates how an on-device agent might gather new vocabulary.

local lexicon = {}

function add_word(word, meaning)
    lexicon[word] = meaning
end

function list_words()
    for w,m in pairs(lexicon) do
        print(w .. ' = ' .. m)
    end
end

return {
    add_word = add_word,
    list_words = list_words
}
