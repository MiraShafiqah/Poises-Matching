# Poises-Matching
This algorithm is an attempt to match students in a group of 4 to 6 people with overlapping understanding and interest

#create_knowledge_graph:

##How the weights are determined. 

o	Intra-category connections: Majors within the same broad category (e.g., STEM, Life Sciences) are connected with a weight of 0.7, indicating strong relationships. 
o	Inter-category connections: Specific connections between related majors across categories are defined in the interdisciplinary_connections list. The weights for these connections range from 0.3 to 0.9, based on the perceived strength of the relationship.

1)	The weights range from 0 to 1, where 1 represents the strongest possible connection and 0 represents no connection.
2)	Within categories (0.8): 
-	Majors within the same category (e.g., all STEM majors) are given a weight of 0.8, indicating strong relationships.
3)	Closely related majors across categories (0.7 - 0.9): 
-	For example, Computer Science and Mathematics are given a weight of 0.9 due to their very strong relationship.
-	Physics and Mathematics also have a 0.9 weight for the same reason.
-	Chemistry and Biology have a 0.7 weight, indicating a strong but slightly less fundamental connection.
4)	Moderately related majors (0.5 - 0.6): 
-	For instance, Psychology and Biology have a 0.6 weight, acknowledging their connection through neuroscience and behavioural studies.
-	Linguistics and Computer Science have a 0.5 weight, reflecting their connection through natural language processing.
5)	Weakly related majors (0.2 - 0.4):
-	Computer Science and Fine Arts have a 0.3 weight, representing potential connections through digital art or computer graphics.
-	Biology and History have a 0.2 weight, indicating a weak connection (perhaps through the history of science).
6)	Unconnected majors (0):
-	Majors with no direct edge between them are considered unconnected in this model.

##Interest tabulation:
####Primary Interest
>> p_interests = set(student1['Primary Interests']) & set(student2['Primary Interests']) score += >>len(p_interests) * 0.5
1)	set(student1['Primary Interests']) creates a set of the primary interests for student1. 
2)	set(student2['Primary Interests']) does the same for student2. 
3)	The & operator finds the intersection of these two sets, i.e., the common primary interests.
4)	len(p_interests) counts how many common primary interests there are. 
5)	This count is multiplied by 0.5 and added to the score. 
6)	The 0.5 multiplier gives less weight to primary interest overlap compared to major compatibility.

####Secondary Interest
>> s_interest = set(student1['Secondary Interests']) & set(student2['Secondary Interests'])
>>score += len(s_interest)
1)	This works similarly to the primary interest calculation. 
2)	The difference is that the count of common secondary interests is added to the score without any multiplier. 
3)	This means that secondary interest overlap is given more weight than primary interest overlap in the compatibility score.
The rationale behind this scoring:
1.	Both primary and secondary interests contribute to the compatibility score, encouraging diverse but related interests in groups.
2.	Secondary interests are weighted more heavily than primary interests. This might be because: 
o	Secondary interests could represent a broader range of topics, increasing the chance of finding common ground.
o	It encourages grouping students with diverse primary interests (possibly related to their majors) but common secondary interests, promoting interdisciplinary connections.
Timezone
1) Calculates the time difference as before. 
2) If the time difference is between 1 and 3 hours: 
•	Adds a small bonus (1 point) to the score. This encourages some time zone diversity while still keeping times close.
3) If the time difference is between 6 and 9 hours: 
•	Adds a larger bonus (2 points) to the score. This favors your preferred range, encouraging diversity from different parts of the world while still allowing for reasonable meeting times.
4) If the time difference is more than 9 hours: 
•	Applies a small penalty. The penalty increases as the time difference grows beyond 9 hours. This discourages extreme time differences that might make scheduling very difficult.

