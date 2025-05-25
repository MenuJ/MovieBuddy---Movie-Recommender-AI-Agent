import streamlit as st
import re
import random
from streamlit_lottie import st_lottie
import requests

# === Memory storage ===
if 'user_preferences' not in st.session_state:
    st.session_state['user_preferences'] = {}
if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = []

# === Helper functions ===
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

def extract_title_director(movie_string):
    """Extract title and director from a movie string format 'Title (Year) by Director'"""
    pattern = r"(.*?)\s*\((\d{4})\)\s*by\s*(.*)"
    match = re.match(pattern, movie_string)
    if match:
        return {
            'title': match.group(1).strip(),
            'year': match.group(2),
            'director': match.group(3).strip()
        }
    return {'title': movie_string, 'year': 'N/A', 'director': 'Unknown'}

def get_recommendations(preferences):
    """Generate movie recommendations based on genre preferences."""
    genre_recommendations = {
        "action": [
            "The Fast and the Furious (2001) by Rob Cohen",
            "Drive (2011) by Nichols Winding Refn",
            "Predator (1987) by John McTiernan",
            "First Blood (1982) by Ted Kotcheff",
            "Armageddon (1998) by Michael Bay",
            "The Avengers (2012) by Joss Whedon",
            "Spider-Man (2002) by Sam Raimi",
            "Batman (1989) by Tim Burton",
            "Enter the Dragon (1973) by Robert Clouse",
            "Crouching Tiger, Hidden Dragon (2000) by Ang Lee",
            "Inception (2010) by Christopher Nolan",
            "Lethal Weapon (1987) by Richard Donner",
            "Yojimbo (1961) by Akira Kurosawa",
            "Superman (1978) by Richard Donner",
            "Wonder Woman (2017) by Patty Jenkins",
            "Black Panther (2018) by Ryan Coogler",
            "Mad Max (1979-2014) by George Miller",
            "Top Gun (1986) by Tony Scott",
            "Mission: Impossible (1996) by Brian DePalma",
            "The Bourne Trilogy (2002-2007) by Paul Greengrass",
            "Goldfinger (1964) by Guy Hamilton",
            "The Terminator (1984-1991) by James Cameron",
            "The Dark Knight (2008) by Christopher Nolan",
            "The Matrix (1999) by The Wachowskis",
            "Die Hard (1988) by John McTiernan"
            
        ],
        "adventure": [
            "The Goonies (1985) by Richard Donner",
            "Gunga Din (1939) by George Stevens",
            "Road to Morocco (1942) by David Butler",
            "The Poseidon Adventure (1972) by Ronald Neame",
            "Fitzcarraldo (1982) by Werner Herzog",
            "Cast Away (2000) by Robert Zemeckis",
            "Life of Pi (2012) by Ang Lee",
            "The Revenant (2015) by Alejandro G. Inarritu",
            "Aguirre, Wrath of God (1972) by Werner Herzog",
            "Mutiny on the Bounty (1935) by Frank Lloyd",
            "Pirates of the Caribbean (2003) by Gore Verbinski",
            "The Adventures of Robin Hood (1938) by Michael Curtiz",
            "The African Queen (1951) by John Huston",
            "To Have and Have Not (1944) by Howard Hawks",
            "L’Atalante (1934) by Jean Vigo",
            "The Right Stuff (1983) by Philip Kaufman",
            "Apollo 13 (1995) by Ron Howard",
            "Gravity (2013) by Alfonso Cuaron",
            "The Princess Bride (1987) by Rob Reiner",
            "The Wages of Fear (1953) by Henri-Georges Clouzot",
            "The Treasure of the Sierra Madre (1948) by John Huston",
            "Jurassic Park (1993) by Steven Spielberg",
            "King Kong (1933) by Merian Cooper & Ernest Schoedsack",
            "North by Northwest (1959) by Alfred Hitchcock",
            "Raiders of the Lost Ark (1981) by Steven Spielberg"
        ],
        "animation":[
            "The Land Before Time (1988) by Don Bluth",
            "Moana (2016) by Ron Clements, John Musker",
            "My Neighbor Totoro (1988) by Hayao Miyazaki",
            "The Incredibles (2004) by Brad Bird",
            "The Nightmare Before Christmas (1993) by Tim Burton",
            "Inside Out (2015) by Pete Docter, Ronnie Del Carmen",
            "Bambi (1942) by Walt Disney",
            "Aladdin (1992) by Ron Clements, John Musker",
            "Sleeping Beauty (1959) by Walt Disney",
            "Frozen (2013) by Chris Buck, Jennifer Lee",
            "Fantasia (1940) by Walt Disney",
            "Up (2009) by Pete Docter, Bob Peterson",
            "The Jungle Book (1967) by Walt Disney",
            "Finding Nemo (2003) by Andrew Stanton, Lee Unkrich",
            "The Little Mermaid (1989) by Ron Clements, John Musker",
            "Cinderella (1950) by Walt Disney",
            "Shrek (2001) by Andrew Adamson, Vicky Jenson",
            "WALL-E (2008) by Andrew Stanton",
            "Pinocchio (1940) by Walt Disney",
            "Spirited Away (2001) by Hayao Miyazaki",
            "Beauty and the Beast (1991) by Gary Trousdale, Kirk Wise",
            "Who Framed Roger Rabbit? (1988) by Robert Zemeckis",
            "Toy Story (1995) by John Lasseter",
            "Snow White & The Seven Dwarfs (1937) by Walt Disney",
            "The Lion King (1994) by Roger Allers, Rob Minkoff"
        ],
        "biopic":[
            "The King’s Speech (2008) by Tom Hooper",
            "Darkest Hour (2017) by Joe Wright",
            "Yankee Doodle Dandy (1942) by Michael Curtiz",
            "Hidden Figures (2016) by Theodore Melfi",
            "A Beautiful Mind (2001) by Ron Howard",
            "The Imitation Game (2014) by Morten Tyldum",
            "My Left Foot (1989) by Jim Sheridan",
            "The Miracle Worker (1962) by Arthur Penn",
            "Capote (2004) by Bennett Miller",
            "Captain Phillips (2013) by Paul Greengrass",
            "The Pride of the Yankees (1942) by Sam Wood",
            "Coal Miner’s Daughter (1980) by Michael Apted",
            "Straight Outta Compton (2015) by F. Gary Gray",
            "Walk the Line (2005) by James Mangold",
            "Ray (2004) by Taylor Hackford",
            "Gospel According to St. Matthew (1964) by Pier Pasolini",
            "Norma Rae (1979) by Martin Ritt"
            "The Elephant Man (1980) by David Lynch",
            "Selma (2014) by Ava DuVernay",
            "Lincoln (2012) by Steven Spielberg",
            "Gandhi (1982) by Richard Attenborough",
            "Malcolm X (1992) by Spike Lee",
            "The Social Network (2010) by David Fincher",
            "Raging Bull (1980) by Martin Scorsese",
            "Schindler’s List (1993) by Steven Spielberg"
        ],
        "comedy": [
          "Bridesmaids (2011) by Paul Feig",
          "Clerks (1994) by Kevin Smith",
          "The Nutty Professor (1963) by Jerry Lewis",
          "Beverly Hills Cop (1984) by Martin Brest",
          "The Odd Couple (1968) by Gene Saks",
          "The Music Box (1932) by James Parrott",
          "There’s Something About Mary (1998) by Farrelly Brothers",
          "This is Spinal Tap! (1984) by Rob Reiner",
          "Office Space (1999) by Mike Judge",
          "The Naked Gun (1988) by Zucker, Abrahams, Zucker",
          "Ghostbusters (1984) by Ivan Reitman",
          "The Hangover (2009) by Todd Phillips",
          "Young Frankenstein (1974) by Mel Brooks",
          "The Big Lebowski (1998) by Coen Brothers",
          "The 40-Year-Old Virgin (2005) by Judd Apatow",
          "Wedding Crashers (2005) by David Dobkin",
          "The Jerk (1979) by Carl Reiner",
          "Dumb and Dumber (1994) by Farrelly Brothers",
          "Animal House (1978) by John Landis",
          "Austin Powers (1997) by Jay Roach",
          "Monty Python Holy Grail (1975) by Terry Gilliam, Terry Jones",
          "Airplane! (1980) by Zucker, Abrahams, Zucker",
          "Duck Soup (1933) by Leo McCarey",
          "Caddyshack (1980) by Harold Ramis",
          "Blazing Saddles (1974) by Mel Brooks"  
        ],
        "coming of age": [
            "American Pie (1999) by Paul Weitz",
            "Whiplash (2014) by Damien Chazelle",
            "Dead Poets Society (1989) by Peter Weir",
            "Saturday Night Fever (1977) by John Badham",
            "Closely Watched Trains (1966) by Jiri Menzel",
            "Amarcord (1973) by Federico Fellini",
            "Boyz N the Hood (1991) by John Singleton",
            "Short Term 12 (2013) by Destin Daniel Cretton",
            "Pather Panchali (1955) by Satyajit Ray",
            "Stand By Me (1986) by Rob Reiner",
            "Ferris Bueller’s Day Off (1986) by John Hughes",
            "Dazed and Confused (1993) by Richard Linklater",
            "Y Tu Mama También (2001) by Alfonso Cuaron",
            "Diner (1982) by Barry Levinson",
            "Lady Bird (2017) by Greta Gerwig",
            "The Breakfast Club (1985) by John Hughes",
            "Moonlight (2016) by Barry Jenkins",
            "The Last Picture Show (1971) by Peter Bogdanovich",
            "Good Will Hunting (1997) by Gus Van Sant",
            "Rebel Without a Cause (1955) by Nicholas Ray",
            "Fast Times at Ridgemont High (1982) by Amy Heckerling",
            "The 400 Blows (1959) by Francois Truffaut",
            "American Graffiti (1973) by George Lucas",
            "Boyhood (2014) by Richard Linklater",
            "The Graduate (1967) by Mike Nichols"
        ],
        "courtroom": [
          "The Accused (1988) by Jonathan Kalpan",
          "Primal Fear (1996) by Gregory Hoblit",
          "Legally Blonde (2001) by Robert Luketic",
          "Disorder in the Court (1936) by Jack White",
          "My Cousin Vinny (1992) by Jonathan Lynn",
          "Loving (2016) by Jeff Nichols",
          "A Time to Kill (1996) by Joel Schumacher",
          "Inherit the Wind (1960) by Stanley Kramer",
          "And Justice for All (1979) by Norman Jewison",
          "Miracle on 34th Street (1947) by George Seaton",
          "JFK (1991) by Oliver Stone",
          "Erin Brockovich (2000) by Steven Soderbergh",
          "Paths of Glory (1957) by Stanley Kubrick",
          "Anatomy of a Murder (1959) by Otto Preminger",
          "Judgment at Nuremberg (1961) by Stanley Kramer",
          "Witness for the Prosecution (1957) by Billy Wilder",
          "A Cry in the Dark (1988) by Fred Schepisi",
          "Adam’s Rib (1949) by George Cukor",
          "Kramer vs. Kramer (1979) by Robert Benton",
          "Rashomon (1950) by Akira Kurosawa",
          "A Few Good Men (1992) by Rob Reiner",
          "12 Angry Men (1957) by Sidney Lumet",
          "Philadelphia (1993) by Jonathan Demme",
          "The Verdict (1982) by Sidney Lumet",
          "To Kill a Mockingbird (1962) by Robert Mulligan"  
        ],
        "crime": [
          "Hell or High Water (2016) by David McKenzie",
          "In Cold Blood (1967) by Richard Brooks",
          "Pink Flamingos (1972) by John Waters",
          "A Fish Called Wanda (1988) by Charles Crichton",
          "Training Day (2001) by Antoine Fuqua",
          "Serpico (1973) by Sidney Lumet",
          "Shaft (1973) by Gordon Parks Jr.",
          "Heat (1995) by Michael Mann",
          "Wall Street (1987) by Oliver Stone",
          "La Haine (1995) by Mathieu Kassovitz",
          "Ocean’s Eleven (2001) by Steven Soderbergh",
          "Run Lola Run (1998) by Tom Tykwer",
          "The Fugitive (1993) by Andrew Davis",
          "Bullitt (1968) by Peter Yates",
          "Dirty Harry (1971) by Don Siegel",
          "American Hustle (2011) by David O. Russell",
          "The Sting (1973) by George Roy Hill",
          "Fight Club (1999) by David Fincher",
          "City of God (2002) by Fernando Meirelles & Katia Lund",
          "The French Connection (1971) by William Friedkin",
          "Dog Day Afternoon (1975) by Sidney Lumet",
          "No Country for Old Men (2007) by Coen Brothers",
          "Breathless (1960) by Jean-Luc Godard",
          "Fargo (1996) by Coen Brothers",
          "Taxi Driver (1976) by Martin Scorsese"
        ],
        "documentary": [
         "Sherman’s March (1985) by Ross McElwee",
         "I Am Not Your Negro (2016) by Raoul Peck",
         "Harlan County, USA (1976) by Barbara Kopple",
         "Borat: Cultural Learnings of America (2006) by Larry Charles",
         "Taxi to the Dark Side (2001) by Alex Gibney",
         "Citizenfour (2014) by Laura Poitras",
         "Don’t Look Back (1967) by D.A. Pennebaker",
         "20 Feet from Stardom (2013) by Morgan Neville",
         "Blackfish (2013) by Gabriela Cowperthwaite",
         "The Silent World (1956) by Jacques Cousteau, Louis Malle",
         "Grizzly Man (2005) by Werner Herzog",
         "An Inconvenient Truth (2006) by Davis Guggenheim",
         "Triumph of the Will (1935) by Leni Riefenstahl",
         "Shoah (1985) by Claude Lanzmann",
         "The Act of Killing (2012) by Joshua Oppenheimer",
         "Bowling for Columbine (2002) by Michael Moore",
         "Nanook of the North (1922) by Robert J. Flaherty",
         "Man on Wire (2008) by James Marsh",
         "Gates of Heaven (1978) by Errol Morris",
         "Salesman (1968) by Albert & David Maysles",
         "Titicut Follies (1967) by Frederick Wiseman",
         "Hoop Dreams (1994) by Steve James",
         "Up (1984-2012) by Paul Almond & Michael Apted",
         "The Thin Blue Line (1988) by Errol Morris",
         "Night and Fog (1955) by Alain Resnais"
        ],
        "drama": [
            "Stranger Than Paradise (1984) by Jim Jarmusch",
            "Paris, Texas (1984) by Wim Wenders",
            "Black Narcissus (1947) by Powell & Pressburger",
            "Crash (2005) by Paul Haggis",
            "Cleo from 5 to 7 (1957) by Agnes Varda",
            "Central Station (1998) by Walter Salles",
            "The Help (2011) by Tate Taylor",
            "Raise the Red Lantern (1991) by Yimou Zhang",
            "The Elements Trilogy (1996-2005) by Deepa Metah",
            "Magnolia (1999) by Paul Thomas Anderson",
            "The Earrings of Madame De… (1953) by Max Ophuls",
            "Au Hasard Balthazar (1966) by Robert Bresson",
            "Three Colors Trilogy (1993-1994) by Krzysztof Kieslowski",
            "The Lost Weekend (1945) by Billy Wilder",
            "Trainspotting (1996) by Danny Boyle",
            "Requiem for a Dream (2000) by Darren Aronofsky",
            "Easy Rider (1969) by Dennis Hopper",
            "Wild Strawberries (1957) by Ingmar Bergman",
            "Nashville (1975) by Robert Altman",
            "Bicycle Thieves (1948) by Vittorio de Sica",
            "On the Waterfront (1954) by Elia Kazan",
            "The Rules of the Game (1939) by Jean Renoir",
            "La Dolce Vita (1960) by Federico Fellini",
            "Do the Right Thing (1989) by Spike Lee",
            "Midnight Cowboy (1969) by John Schlesinger"
        ],
        "epic": [
          "The Passion of the Christ (2004) by Mel Gibson",
          "Cleopatra (1963) by Joseph Mankiewicz",
          "The English Patient (1996) by Anthony Minghella",
          "Out of Africa (1985) by Sydney Pollack",
          "Farewell My Concubine (1993) by Kaige Chen",
          "The Ten Commandments (1956) by Cecil B. DeMille",
          "The Leopard (1963) by Luchino Visconti",
          "Reds (1981) by Warren Beatty",
          "The Last Emperor (1987) by Bernardo Bertolucci",
          "Hamlet (1948) by Laurence Olivier",
          "Ran (1985) by Akira Kurosawa",
          "Amadeus (1984) by Milos Forman",
          "Twelve Years a Slave (2011) by Steve McQueen",
          "The Last of the Mohicans (1992) by Michael Mann",
          "Spartacus (1960) by Stanley Kubrick",
          "Gladiator (2000) by Ridley Scott",
          "Ben-Hur (1959) by William Wyler",
          "Braveheart (1995) by Mel Gibson",
          "Dances with Wolves (1990) by Kevin Costner",
          "Doctor Zhivago (1965) by David Lean",
          "Titanic (1997) by James Cameron",
          "Gone with the Wind (1939) by Victor Fleming",
          "Giant (1956) by George Stevens",
          "The Seven Samurai (1954) by Akira Kurosawa",
          "Lawrence of Arabia (1962) by David Lean"
        ],
        "family comedy": [
            "The Kids Are All Right (2010) by Lisa Cholodenko",
            "Terms of Endearment (1983) by James L. Brooks",
            "Driving Miss Daisy (1989) by Bruce Beresford",
            "The Squid & The Whale (2005) by Noah Baumbach",
            "The Birdcage (1996) by Mike Nichols",
            "Silver Linings Playbook (2012) by David O. Russell",
            "Captain Fantastic (2016) by Matt Ross",
            "My Big Fat Greek Wedding (2002) by Joel Zwick",
            "Moonstruck (1987) by Norman Jewison",
            "Father of the Bride (1950) by Vincente Minnelli",
            "Home Alone (1990) by Chris Columbus",
            "Planes, Trains & Automobiles (1987) by John Hughes",
            "The Way Way Back (2013) by Nat Faxon, Jim Rash",
            "Crimes & Misdemeanors (1989) by Woody Allen",
            "The Descendants (2011) by Alexander Payne",
            "The Royal Tenenbaums (2001) by Wes Anderson",
            "Juno (2007) by Jason Reitman",
            "Hannah and Her Sisters (1986) by Woody Allen",
            "Mrs. Doubtfire (1993) by Chris Columbus",
            "Guess Who’s Coming to Dinner? (1967) by Stanley Kramer",
            "Meet the Parents (2000) by Jay Roach",
            "Rain Man (1988) by Barry Levinson",
            "Little Miss Sunshine (2006) by Jon Dayton, Valerie Faris",
            "Vacation (1983) by Harold Ramis",
            "A Christmas Story (1983) by Bob Clark"
        ],
        "family drama": [
         "Manchester by the Sea (2016) by Kenneth Lonergan",
         "On Golden Pond (1981) by Mark Rydell",
         "Amour (2011) by Michael Haneke",
         "The Color Purple (1985) by Steven Spielberg",
         "Cat on a Hot Tin Roof (1958) by Richard Brooks",
         "Belle de Jour (1967) by Luis Bunuel",
         "The Spirit of the Beehive (1973) by Victor Eurice",
         "The Magnificent Ambersons (1942) by Orson Welles",
         "Days of Heaven (1978) by Terrence Malick",
         "Mudbound (2017) by Dee Rees",
         "The Grapes of Wrath (1940) by John Ford",
         "Secrets & Lies (1996) by Mike Leigh",
         "Sex, Lies & Videotape (1989) by Steven Soderbergh",
         "Scenes from a Marriage (1974) by Ingmar Bergman",
         "A Woman Under the Influence (1974) by John Cassavetes",
         "The Tree of Life (2011) by Terrence Malick",
         "A Separation (2011) by Asghar Farhadi",
         "Ordet (1955) by Carl Theodore Dreyer",
         "Breaking the Waves (1996) by Lars Von Trier",
         "Who’s Afraid of Virginia Woolf? (1966) by Mike Nichols",
         "A Streetcar Named Desire (1951) by Elia Kazan",
         "Written on the Wind (1956) by Douglas Sirk",
         "Ordinary People (1980) by Robert Redford",
         "American Beauty (1999) by Sam Mendes",
         "Tokyo Story (1953) by Yasujirô Ozu"  
        ],
        "fantasy": [
            "Harry Potter (2001) by Chris Columbus",
            "Curious Case of Benjamin Button (2008) by David Fincher",
            "Discreet Charm of the Bourgeoisie (1972) by Luis Bunuel",
            "Being John Malkovich (1999) by Spike Jonze",
            "The Red Balloon (1956) by Albert Lamorisse",
            "Avatar (2009) by James Cameron",
            "Harvey (1950) by Henry Koster",
            "Ghost (1990) by Jerry Zucker",
            "Wings of Desire (1987) by Wim Wenders",
            "Big (1988) by Penny Marshall",
            "Celine & Julie Go Boating (1974) by Jacques Rivette",
            "Willy Wonka & The Chocolate Factory (1971) by Mel Stuart",
            "Ugetsu (1953) by Kenji Mizoguchi",
            "The Purple Rose of Cairo (1985) by Woody Allen",
            "Edward Scissorhands (1990) by Tim Burton",
            "The Red Shoes (1948) by Powell & Pressburger",
            "Beauty and the Beast (1946) by Jean Cocteau",
            "Amelie (2001) by Jean-Pierre Jeunet",
            "The Seventh Seal (1954) by Ingmar Bergman",
            "Pan's Labyrinth (2006) by Guillermo del Toro",
            "Lord of the Rings (2001-2003) by Peter Jackson",
            "Field of Dreams (1989) by Phil Alden Robinson",
            "Groundhog Day (1993) by Harold Ramis",
            "Forrest Gump (1994) by Robert Zemeckis",
            "It’s a Wonderful Life (1946) by Frank Capra"
        ],
        "film noir": [
          "The Postman Always Rings Twice (1946) by Tay Garnett",
          "Murder, My Sweet (1944) by Edward Dmytryck",
          "Point Blank (1967) by John Boorman"
          "The Killers (1946) by Robert Siodmark",
          "In a Lonely Place (1950) by Nicholas Ray",
          "The Lady from Shanghai (1947) by Orson Welles",
          "The Long Goodbye (1973) by Robert Altman",
          "Gun Crazy (1950) by Joseph H. Lewis",
          "They Live By Night (1948) by Nicholas Ray",
          "The Big Heat (1953) by Fritz Lang",
          "The Killing (1956) by Stanley Kubrick",
          "Pickup on South Street (1953) by Sam Fuller",
          "The Night of the Hunter (1955) by Charles Laughton",
          "The Big Sleep (1946) by Howard Hawks",
          "Body Heat (1981) by Lawrence Kasdan",
          "L.A. Confidential (1997) by Curtis Hanson",
          "Mildred Pierce (1945) by Michael Curtiz",
          "Sweet Smell of Success (1957) by Alexander Mackendrick",
          "Out of the Past (1947) by Jacques Tourneur",
          "Laura (1944) by Otto Preminger",
          "Touch of Evil (1958) by Orson Welles",
          "The Maltese Falcon (1941) by John Huston",
          "The Third Man (1949) by Carol Reed",
          "Double Indemnity (1944) by Billy Wilder",
          "Chinatown (1974) by Roman Polanski"
        ],
        "gangster": [
           "Black Mass (2015) by Scott Cooper",
           "Casino (1995) by Martin Scorsese",
           "Road to Perdition (2002) by Sam Mendes",
           "Miller’s Crossing (1990) by Coen Brothers",
           "Carlito’s Way (1993) by Brian De Palma",
           "Once Upon a Time in America (1984) by Sergio Leone",
           "Badlands (1973) by Terrence Malick",
           "Atlantic City (1980) by Louis Malle",
           "Le Samourai (1967) by Jean-Pierre Melville",
           "Leon: The Professional (1994) by Luc Besson",
           "Mean Streets (1973) by Martin Scorsese",
           "Reservoir Dogs (1992) by Quentin Tarantino",
           "The Departed (2005) by Martin Scorsese",
           "American Gangster (2007) by Ridley Scott",
           "The Untouchables (1987) by Brian De Palma",
           "The Public Enemy (1931) by William Wellman",
           "Little Caesar (1930) by Mervyn LeRoy",
           "Scarface: The Shame of a Nation (1932) by Howard Hawks",
           "Thelma & Louise (1991) by Ridley Scott",
           "Bonnie & Clyde (1967) by Arthur Penn",
           "Scarface (1983) by Brian De Palma",
           "White Heat (1949) by Raoul Walsh",
           "Pulp Fiction (1994) by Quentin Tarantino",
           "GoodFellas (1990) by Martin Scorsese",
           "The Godfather I & II (1972-1974) by Francis Ford Coppola"
        ],
        "horror": [
          "The Evil Dead (1981-1987) by Sam Raimi",
          "An American Werewolf in London (1981) by John Landis",
          "Eyes Without a Face (1960) by Georges Franju",
          "The Thing (1982) by John Carpenter",
          "The Fly (1986) by David Cronenberg",
          "Friday the 13th (1980) by Sean Cunningham",
          "A Nightmare on Elm Street (1984) by Wes Craven",
          "Repulsion (1965) by Roman Polanski",
          "Suspiria (1977) by Dario Argento",
          "The Haunting (1963) by Robert Wise",
          "Poltergeist (1982) by Tobe Hooper",
          "Let the Right One In (2008) by Tomas Alfredson",
          "Dracula (1931) by Tod Browning",
          "Frankenstein (1931-1935) by James Whale",
          "The Texas Chainsaw Massacre (1974) by Tobe Hooper",
          "Night of the Living Dead (1968) by George Romero",
          "Scream (1996) by Wes Craven",
          "Halloween (1978) by John Carpenter",
          "Carrie (1976) by Brian De Palma",
          "The Omen (1976) by Richard Donner",
          "Jaws (1975) by Steven Spielberg",
          "The Shining (1980) by Stanley Kubrick",
          "Rosemary’s Baby (1968) by Roman Polanski",
          "Psycho (1960) by Alfred Hitchcock",
          "The Exorcist (1973) by William Friedkin"
        ],
        "musical": [
          "Seven Brides for Seven Brothers (1954) by Stanley Donen",
          "The Rocky Horror Picture Show (1975) by Jim Sharman",
          "Guys and Dolls (1955) by Joseph Mankiewicz",
          "White Christmas (1954) by Michael Curtiz"
          "The Band Wagon (1953) by Vincente Minnelli",
          "Chicago (2002) by Rob Marshall",
          "Oliver! (1968) by Carol Reed",
          "The Gold Diggers Trilogy (1933) by Busby Berkeley",
          "Funny Girl (1968) by William Wyler",
          "Top Hat (1935) by Mark Sandrich",
          "Swing Time (1936) by George Stevens",
          "Moulin Rouge! (2001) by Baz Luhrmann",
          "An American in Paris (1951) by Vincente Minnelli",
          "My Fair Lady (1964) by George Cukor",
          "The King and I (1956) by Walter Lang",
          "Meet Me in St. Louis (1944) by Vincente Minnelli",
          "Cabaret (1972) by Bob Fosse",
          "The Umbrellas of Cherbourg (1964) by Jacques Demy",
          "La La Land (2016) by Damien Chazelle",
          "Grease (1978) by Randal Kleiser",
          "Mary Poppins (1964) by Walt Disney",
          "The Sound of Music (1965) by Robert Wise",
          "West Side Story (1961) by Robert Wise",
          "Singin’ in the Rain (1952) by Stanley Donen & Gene Kelly",
          "The Wizard of Oz (1939) by Victor Fleming"
        ],
        "mystery": [
          "Murder on the Orient Express (1974) by Sidney Lumet",
          "The Lady Vanishes (1938) by Alfred Hitchcock",
          "A Shot in the Dark (1964) by Blake Edwards",
          "The Thin Man (1934) by W.S. Van Dyke",
          "Mystic River (2002) by Clint Eastwood",
          "Zodiac (2007) by David Fincher",
          "Prisoners (2013) by Denis Villeneuve",
          "Rebecca (1940) by Alfred Hitchcock",
          "Girl with the Dragon Tattoo (2009) by Niels Arden Oplev",
          "Gone Girl (2014) by David Fincher",
          "The Vanishing (1988) by George Sluizer",
          "The Crying Game (1992) by Neil Jordan",
          "L’Avventura (1960) by Michelangelo Antonioni",
          "Mulholland Drive (2001) by David Lynch",
          "The Usual Suspects (1995) by Bryan Singer",
          "In the Heat of the Night (1967) by Norman Jewison",
          "Talk to Her (2002) by Pedro Almodóvar",
          "The Conversation (1974) by Francis Ford Coppola",
          "Caché (2005) by Michael Haneke",
          "Blow-Up (1966) by Michelangelo Antonioni",
          "Memento (2000) by Christopher Nolan",
          "Blue Velvet (1986) by David Lynch",
          "Rear Window (1954) by Alfred Hitchcock",
          "Se7en (1996) by David Fincher",
          "Vertigo (1958) by Alfred Hitchcock"
        ],
        "politics and media": [
           "The American President (1995) by Rob Reiner",
           "Good Bye Lenin! (2003) by Wolfgang Becker",
           "The Parallax View (1974) by Alan J. Pakula",
           "The China Syndrome (1979) by James Bridges",
           "Three Days of the Condor (1975) by Sydney Pollack",
           "Good Night and Good Luck (2005) by George Clooney",
           "All the King’s Men (1949) by Robert Rossen",
           "The Great Dictator (1940) by Charlie Chaplin",
           "Nightcrawler (2014) by Dan Gilroy",
           "Broadcast News (1987) by James L. Brooks",
           "The Post (2017) by Steven Spielberg",
           "Seven Days in May (1964) by John Frankenheimer",
           "Being There (1979) by Hal Ashby",
           "Dr. Strangelove (1964) by Stanley Kubrick",
           "Ace in the Hole (1951) by Billy Wilder",
           "Spotlight (2015) by Tom McCarthy",
           "Z (1969) by Costa-Gavras",
           "The Conformist (1970) by Bernardo Bertolucci",
           "A Face in the Crowd (1957) by Elia Kazan",
           "The Manchurian Candidate (1962) by John Frankenheimer",
           "Mr. Smith Goes to Washington (1939) by Frank Capra",
           "His Girl Friday (1940) by Howard Hawks",
           "Network (1976) by Sidney Lumet",
           "All the President's Men (1976) by Alan J. Pakula",
           "Citizen Kane (1941) by Orson Welles" 
        ],
        "prison": [
          "Kiss of the Spider Woman (1985) by Hector Babenco",
          "In the Name of the Father (1993) by Jim Sheridan",
          "Dead Man Walking (1995) by Tim Robbins",
          "The Longest Yard (1974) by Robert Aldrich",
          "I’m a Fugitive from a Chain Gang (1932) by Mervyn LeRoy",
          "American History X (1998) by Tony Kaye",
          "The Defiant Ones (1958) by Stanley Kramer",
          "Down By Law (1986) by Jim Jarmusch",
          "Stalag 17 (1953) by Billy Wilder",
          "A Prophet (2009) by Jacques Audiard",
          "Son of Saul (2015) by Laszlo Nemes",
          "Papillon (1973) by Franklin J. Schaffner",
          "The Hurricane (1999) by Norman Jewison",
          "Birdman of Alcatraz (1962) by John Frankenheimer",
          "Escape from Alcatraz (1979) by Don Siegel",
          "The Green Mile (1999) by Frank Darabont",
          "Life is Beautiful (1997) by Roberto Benigni",
          "Sophie’s Choice (1982) by Alan J. Pakula",
          "La Grand Illusion (1937) by Jean Renoir",
          "A Man Escaped (1956) by Robert Bresson",
          "The Bridge on the River Kwai (1957) by David Lean",
          "The Great Escape (1963) by John Sturges",
          "Cool Hand Luke (1967) by Stuart Rosenberg",
          "One Flew Over the Cuckoo’s Nest (1975) by Milos Forman",
          "The Shawshank Redemption (1994) by Frank Darabont"
        ],
        "romance": [
          "The Notebook (2004) by Nick Cassavetes",
          "An Officer and a Gentleman (1982) by Taylor Hackford",
          "Dirty Dancing (1987) by Emile Ardolino",
          "The Quiet Man (1952) by John Ford",
          "Carol (2015) by Todd Haynes",
          "Letter from an Unknown Woman (1948) by Max Ophuls",
          "Remains of the Day (1992) by James Ivory",
          "Shakespeare in Love (1998) by John Madden",
          "Wuthering Heights (1939) by William Wyler",
          "The Piano (1993) by Jane Campion",
          "Witness (1985) by Peter Weir",
          "Before Trilogy (1995-2013) by Richard Linklater",
          "Jules and Jim (1962) by Francois Truffaut",
          "The Bridges of Madison County (1995) by Clint Eastwood",
          "Harold & Maude (1971) by Hal Ashby",
          "Love Story (1970) by Arthur Hiller",
          "An Affair to Remember (1957) by Leo McCarey",
          "The Way We Were (1973) by Sydney Pollack",
          "In the Mood for Love (2000) by Wong Kar-Wai",
          "Brokeback Mountain (2005) by Ang Lee",
          "Brief Encounter (1945) by David Lean",
          "A Place in the Sun (1951) by George Stevens",
          "Eternal Sunshine of Spotless Mind (2004) by Michel Gondry",
          "Breakfast at Tiffany’s (1961) by Blake Edwards",
          "Casablanca (1942) by Michael Curtiz"
        ],
        "romantic comedy": [
            "The Big Sick (2017) by Michael Showalter",
            "Pillow Talk (1959) by Michael Gordon",
            "Love Actually (2003) by Richard Curtis",
            "Manhattan (1979) by Woody Allen",
            "The Awful Truth (1937) by Leo McCarey",
            "Something’s Gotta Give (2003) by Nancy Meyers",
            "Ninotchka (1939) by Ernst Lubitsch",
            "As Good as It Gets (1997) by James L. Brooks",
            "The Lady Eve (1941) by Preston Sturges",
            "Pretty Woman (1990) by Garry Marshall",
            "Trouble in Paradise (1932) by Ernst Lubitsch",
            "Say Anything (1989) by Cameron Crowe",
            "The Palm Beach Story (1942) by Preston Sturges",
            "Roman Holiday (1953) by William Wyler",
            "Sleepless in Seattle (1993) by Nora Ephron",
            "The Shop Around the Corner (1940) by Ernst Lubitsch",
            "Jerry Maguire (1996) by Cameron Crowe",
            "The Apartment (1960) by Billy Wilder",
            "Bringing Up Baby (1938) by Howard Hawks",
            "Tootsie (1982) by Sydney Pollack",
            "Some Like It Hot (1959) by Billy Wilder",
            "The Philadelphia Story (1940) by George Cukor",
            "It Happened One Night (1934) by Frank Capra",
            "Annie Hall (1977) by Woody Allen",
            "When Harry Met Sally (1989) by Rob Reiner"
        ],
        "science fiction": [
          "Children of Men (2006) by Alfonso Cuaron",
          "Soylent Green (1973) by Richard Fleischer",
          "District 9 (2009) by Neill Blomkamp",
          "Star Trek II: Wrath of Khan (1982) by Nicholas Meyer",
          "Snowpiercer (2011) by Joon-ho Bong",
          "Independence Day (1996) by Roland Emmerich",
          "Arrival (2016) by Denis Villeneuve",
          "Godzilla (1954) by Ishiro Hondo",
          "Total Recall (1990) by Paul Verhoeven",
          "Minority Report (2000) by Steven Spielberg",
          "La Jetee (1962) by Chris Marker",
          "Her (2013) by Spike Jonze",
          "Ex Machina (2014) by Alex Garland",
          "Solaris (1972) by Andrei Tarkovsky",
          "The Day the Earth Stood Still (1951) by Robert Wise",
          "Invasion of the Body Snatchers (1956) by Don Siegel",
          "A Clockwork Orange (1971) by Stanley Kubrick",
          "Blade Runner (1982) by Ridley Scott",
          "Close Encounters of the 3rd Kind (1977) by Steven Spielberg",
          "Planet of the Apes (1968) by Franklin J. Schaffner",
          "E.T. The Extra Terrestrial (1982) by Steven Spielberg",
          "Alien (1979-1986) by Ridley Scott / James Cameron",
          "Back to the Future (1985) by Robert Zemeckis",
          "Star Wars (1977-1980) by George Lucas",
          "2001: A Space Odyssey (1968) by Stanley Kubrick"
        ],
        "showbiz": [
          "Lost in Translation (2004) by Sofia Coppola",
          "A Night at the Opera (1935) by Sam Wood",
          "To Be or Not to Be (1942) by Ernst Lubitsch",
          "Synecdoche, New York (2008) by Charlie Kaufman",
          "A Star is Born (1954) by George Cukor",
          "Whatever Happened to Baby Jane (1962) by Robert Aldrich",
          "Slumdog Millionaire (2008) by Danny Boyle",
          "The Producers (1968) by Mel Brooks",
          "Boogie Nights (1997) by Paul Thomas Anderson",
          "Argo (2012) by Ben Affleck",
          "Ed Wood (1994) by Tim Burton",
          "The Truman Show (1998) by Peter Weir",
          "The Player (1992) by Robert Altman",
          "The Bad and the Beautiful (1952) by Vincente Minnelli",
          "Day for Night (1973) by Francois Truffaut",
          "Cinema Paradiso (1988) by Giuseppe Tornatore",
          "Contempt (1963) by Jean-Luc Godard",
          "Quiz Show (1994) by Robert Redford",
          "Sullivan’s Travels (1941) by Preston Sturges",
          "Persona (1966) by Ingmar Bergman",
          "Birdman (2014) by Alejandro G. Inarritu",
          "All That Jazz (1979) by Bob Fosse",
          "8 1/2 (1963) by Federico Fellini",
          "All About Eve (1950) by Joseph Mankiewicz",
          "Sunset Boulevard (1950) by Billy Wilder"
        ],
        "silent": [
          "A Trip to the Moon (1902) by Georges Melies",
          "The Cabinet of Dr. Caligari (1920) by Robert Wiene",
          "The Thief of Baghdad (1924) by Raoul Walsh",
          "The Jazz Singer (1927) by Alan Crosland ***",
          "The Artist (2011) by Michel Hazanavicius",
          "The Last Laugh (1924) by F.W. Murnau",
          "Un Chien Andalou (1929) by Luis Bunuel, Salvador Dali",
          "The Crowd (1928) by King Vidor",
          "Wings (1927) by William Wellman",
          "Greed (1924) by Erich von Stroheim",
          "The Gold Rush (1925) by Charlie Chaplin",
          "Playtime (1967) by Jacques Tati",
          "Safety Last! (1923) by Fred Newmeyer",
          "Sherlock Jr. (1924) by Buster Keaton",
          "The Birth of a Nation (1915) by D.W. Griffith",
          "Intolerance (1916) by D.W. Griffith",
          "Passion of Joan of Arc (1928) by Carl Theodore Dreyer",
          "City Lights (1931) by Charlie Chaplin",
          "Metropolis (1927) by Fritz Lang",
          "Nosferatu (1922) by F.W. Murnau",
          "Battleship Potemkin (1925) by Sergei Eisenstein",
          "Sunrise (1927) by F.W. Murnau",
          "Man with a Movie Camera (1929) by Dziga Vertov",
          "The General (1926) by Buster Keaton & Clyde Bruckman",
          "Modern Times (1936) by Charlie Chaplin"
        ],
        "sports": [
          "The Karate Kid (1984) by John G. Avildsen",
          "Happy Gilmore (1996) by Dennis Dugan",
          "The Blind Side (2009) by John Lee Hancock",
          "Moneyball (2011) by Bennett Miller",
          "Chariots of Fire (1981) by Hugh Hudson",
          "Friday Night Lights (2004) by Peter Berg",
          "White Men Can’t Jump (1992) by Ron Shelton",
          "North Dallas Forty (1979) by Ted Kotcheff",
          "The Mighty Ducks (1992) by Stephen Herek",
          "The Bad News Bears (1976) by Michael Ritchie",
          "The Sandlot (1993) by David Mickey Evans",
          "Miracle (2004) by Gavin O’Connor",
          "The Natural (1984) by Barry Levinson",
          "Million Dollar Baby (2004) by Clint Eastwood",
          "Breaking Away (1979) by Peter Yates",
          "Major League (1989) by David S. Ward",
          "Slap Shot (1977) by George Roy Hill",
          "The Wrestler (2008) by Darren Aronofsky",
          "The Hustler (1961) by Robert Rossen",
          "Rudy (1993) by David Anspaugh",
          "A League of Their Own (1992) by Penny Marshall",
          "Hoosiers (1986) by David Anspaugh",
          "Bull Durham (1988) by Ron Shelton",
          "Remember the Titans (2000) by Boaz Yakin",
          "Rocky (1976) by John G. Avildsen"
        ],
        "thriller": [
          "Strangers on a Train (1951) by Alfred Hitchcock",
          "Wait Until Dark (1967) by Terrence Young",
          "Dressed to Kill (1980) by Brian De Palma",
          "The 39 Steps (1935) by Alfred Hitchcock",
          "Basic Instinct (1992) by Paul Verhoeven",
          "Room (2013) by Lenny Abrahamson",
          "Jacob’s Ladder (1990) by Adrian Lyne",
          "Dead Ringers (1988) by David Cronenberg",
          "Dial M for Murder (1954) by Alfred Hitchcock",
          "Marathon Man (1976) by John Schlesinger",
          "Misery (1990) by Rob Reiner",
          "Rope (1948) by Alfred Hitchcock",
          "Oldboy (2003) by Chan-wook Park",
          "Cape Fear (1962) by J. Lee Thompson",
          "The Birds (1963) by Alfred Hitchcock",
          "M (1931) by Fritz Lang",
          "Don’t Look Now (1973) by Nicolas Roeg",
          "Black Swan (2010) by Darren Aronofsky",
          "Fatal Attraction (1987) by Adrian Lyne",
          "Deliverance (1972) by John Boorman",
          "Get Out (2017) by Jordan Peele",
          "Les Diabolique (1955) by Henri-Georges Clouzot",
          "The Sixth Sense (1999) by M. Night Shyamalan",
          "Notorious (1946) by Alfred Hitchcock",
          "The Silence of the Lambs (1991) by Jonathan Demme"
        ],
        "war": [
           "The Dirty Dozen (1967) by Robert Aldrich",
           "Inglourious Basterds (2009) by Quentin Tarantino",
           "Downfall (2004) by Oliver Hirschbiegel",
           "From Here to Eternity (1953) by Fred Zinnemann",
           "Good Morning, Vietnam (1987) by Barry Levinson",
           "Dunkirk (2017) by Christopher Nolan",
           "Born on the Fourth of July (1989) by Oliver Stone",
           "Coming Home (1978) by Hal Ashby",
           "Hiroshima Mon Amour (1959) by Alain Resnais",
           "Ashes & Diamonds (1958) by Andrzej Wajda",
           "Rome Open City (1945) by Roberto Rossellini",
           "The Hurt Locker (2009) by Kathryn Bigelow",
           "Das Boot (1981) by Wolfgang Petersen",
           "All Quiet on the Western Front (1930) by Lewis Milestone",
           "M*A*S*H (1970) by Robert Altman",
           "Patton (1970) by Franklin J. Schaffner",
           "Glory (1989) by Edward Zwick",
           "Zero Dark Thirty (2012) by Kathryn Bigelow",
           "The Battle of Algiers (1966) by Gillo Pontecorvo",
           "Platoon (1986) by Oliver Stone",
           "Full Metal Jacket (1987) by Stanley Kubrick",
           "The Deer Hunter (1978) by Michael Cimino",
           "The Best Years of Our Lives (1946) by William Wyler",
           "Saving Private Ryan (1998) by Steven Spielberg",
           "Apocalypse Now (1979) by Francis Ford Coppola"
        ],
        "western": [
          "The Magnificent Seven (1960) by John Sturges",
          "Django Unchained (2012) by Quentin Tarantino",
          "3:10 to Yuma (1957) by Delmer Daves",
          "True Grit (1969) by Henry Hathaway",
          "Winchester ’73 (1950) by Anthony Mann",
          "Tombstone (1993) by George Cosmatos",
          "My Darling Clementine (1946) by John Ford",
          "The Ox-Bow Incident (1943) by William Wellman",
          "Cat Ballou (1965) by Elliot Silverstein",
          "Johnny Guitar (1956) by Nicholas Ray",
          "Red River (1948) by Howard Hawks",
          "The Outlaw Josey Wales (1976) by Clint Eastwood",
          "Stagecoach (1939) by John Ford",
          "There Will Be Blood (2007) by Paul Thomas Anderson",
          "McCabe and Mrs. Miller (1971) by Robert Altman",
          "The Man Who Shot Liberty Valance (1962) by John Ford",
          "Rio Bravo (1959) by Howard Hawks",
          "Unforgiven (1992) by Clint Eastwood",
          "Shane (1953) by George Stevens",
          "Once Upon a Time in the West (1968) by Sergio Leone",
          "High Noon (1952) by Fred Zinnemann",
          "The Wild Bunch (1969) by Sam Peckinpah",
          "Butch Cassidy & Sundance Kid (1969) by George Roy Hill",
          "The Good, The Bad & The Ugly (1966) by Sergio Leone",
          "The Searchers (1956) by John Ford"
        ]
    }

    # Extract genre from preferences string
    genre = None
    if 'genre' in preferences.lower():
        genre_match = re.search(r'genre:\s*([^,]+)', preferences.lower())
        if genre_match:
            genre = genre_match.group(1).strip().lower()

    # Find the closest matching genre
    matching_genre = None
    for key in genre_recommendations.keys():
        if genre and key in genre:
            matching_genre = key
            break

    # Get recommendations based on genre
    if matching_genre:
        recs = list(genre_recommendations[matching_genre])
        random.shuffle(recs)
        return [extract_title_director(recs[i]) for i in range(min(25, len(recs)))]
    else:
        return []

def update_preferences(new_preferences):
    """Update user preferences in session state"""
    st.session_state['user_preferences'] = new_preferences
    st.session_state['recommendations'] = get_recommendations(new_preferences)

# === Main App ===
def main():
    # Set page config
    st.set_page_config(
        page_title="MovieBuddy - Your Personal Movie Recommender",
        page_icon="🎬",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .movie-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .movie-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 8px;
    }
    .movie-info {
        font-style: italic;
        color: #666;
        font-size: 1.1rem;
    }
    .genre-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        height: fit-content;
    }
    .recommendations-section {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1e3c72;
        color: white;
        border: none;
        padding: 0.75rem 0;
        font-size: 1.1rem;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #2a5298;
    }
    .selectbox {
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title section with gradient background
    st.markdown("""
        <div class="title-container">
            <h1>🎬 MovieBuddy</h1>
            <h3>Your Personal Movie Recommendation App</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Load animation
    movie_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_CTaizi.json")
    
    # Title and description
    st.title("🎬 MovieBuddy")
    st.subheader("Your Personal Movie Recommendation App")
    
    # Display animation
    if movie_animation:
        st_lottie(movie_animation, height=250, key="movie_anim")
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    # User preferences section (Left column)
    with col1:
        st.markdown("## 🎥 Choose Genre")
        
        # User inputs for preferences
        genre_input = st.selectbox(
            "What genre do you enjoy?",
            options=[
                "Action", 
                "Adventure", 
                "Animation", 
                "Biopic",
                "Comedy",
                "Coming of Age",
                "Courtroom",
                "Crime",
                "Documentary",
                "Drama",
                "Epic",
                "Family Comedy",
                "Family Drama",
                "Fantasy",
                "Film Noir",
                "Gangster",
                "Horror",
                "Musical",
                "Mystery",
                "Politics and Media",
                "Prison",
                "Romance",
                "Romantic Comedy",
                "Science Fiction",
                "Showbiz",
                "Silent",
                "Sports",
                "Thriller",
                "War",
                "Western"
            ]
        )
        
        if st.button("Get Recommendations", key="get_recs"):
            preferences_str = f"genre: {genre_input}"
            update_preferences(preferences_str)
            st.success("Found the top watched movies for you!")
    
    # Recommendations section (Right column)
    with col2:
        st.markdown("## 🎬 Your Personalized Recommendations")
        
        if st.session_state['recommendations']:
            for i, movie in enumerate(st.session_state['recommendations']):
                movie_key = f"movie_{i}"
                
                with st.container():
                    html_content = f"""
                    <div class="movie-card" id="{movie_key}">
                        <div class="movie-title">{movie['title']} ({movie['year']})</div>
                        <div class="movie-info">Director: {movie['director']}</div>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            if 'user_preferences' in st.session_state and st.session_state['user_preferences']:
                st.info("We couldn't find movies matching your preferences. Try a different genre!")
            else:
                st.info("Select your favorite genre to get personalized movie recommendations!")
    
    # Footer
    st.markdown("---")
    
    # Help section
    with st.expander("ℹ How to use MovieBuddy"):
        st.markdown("""
        1. Select your favorite genre from the dropdown menu
        2. Click 'Get Recommendations' to generate personalized movie recommendations
        3. Enjoy browsing through your personalized movie list!
        """)
    
    st.markdown("Made 🎥 by MMJ | © 2025")

if __name__ == "__main__":
    main()
