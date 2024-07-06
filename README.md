# CA_tech_fest
# Room Allocation System Documentation

This documentation provides an overview of the Python code for a room allocation system that helps in assigning rooms to groups in a hostel based on gender-specific accommodations. The code uses Pandas for data manipulation and regular expressions for gender identification within group descriptions.

## Dependencies

- pandas
- re

Install the dependencies using pip:
```bash
pip install pandas
```
# HOW TO USE
* clone this repository
```
git clone
```
* Change directory to the cloned repository
```
cd CA_tech_fest
```
* run python3 app.py
```
python3 app.py
```
* click on the URL http://127.0.0.1:5000 appeared on the terminal
# DEPLOYED at render.com
* click on https://ca-tech-fest-1.onrender.com/ to use directly

## Functions

### `clean_column_names(df)`

Cleans the column names of a DataFrame by converting them to lowercase and removing spaces.

#### Parameters:
- `df`: `pd.DataFrame` - The DataFrame whose columns need to be cleaned.

#### Returns:
- `pd.DataFrame` - The DataFrame with cleaned column names.

### `split_group_by_gender(group_df)`

Splits the group information by gender, creating separate entries for boys and girls if specified within the group.

#### Parameters:
- `group_df`: `pd.DataFrame` - DataFrame containing group information.

#### Returns:
- `pd.DataFrame` - A new DataFrame with split groups by gender.

### `allocate_rooms(group_file_path, hostel_file_path)`

Allocates rooms to groups based on the information provided in the CSV files for groups and hostels.

#### Parameters:
- `group_file_path`: `str` - The file path to the CSV file containing group information.
- `hostel_file_path`: `str` - The file path to the CSV file containing hostel information.

#### Returns:
- `list` - A list of dictionaries containing the allocation results.

## Example Usage

```python
allocation_result = allocate_rooms('group_file.csv', 'hostel_file.csv')
print(allocation_result)
```

## Detailed Explanation

### Cleaning Column Names

The `clean_column_names` function ensures all column names are lowercase and have no spaces, making it easier to work with them later on.

### Splitting Groups by Gender

The `split_group_by_gender` function takes the group DataFrame and splits the groups by gender if specified. It uses regular expressions to identify the number of boys and girls in each group and creates separate entries for each gender.

### Allocating Rooms

The `allocate_rooms` function is the main function that handles the room allocation process. It follows these steps:

1. **Reading CSV Files**: It reads the group and hostel information from the provided CSV file paths into DataFrames.
2. **Cleaning Column Names**: It cleans the column names using the `clean_column_names` function.
3. **Splitting Groups by Gender**: It splits the groups by gender using the `split_group_by_gender` function.
4. **Allocating Rooms**: It allocates rooms to each group based on gender-specific accommodations. It tries to find an exact match for the group size first and then allocates to the smallest room that can fit the group. If no such room is available, it allocates as many members as possible to the largest available room.

### Handling Allocations

- **Exact Match**: If an exact room capacity match is found, the group is allocated to that room.
- **Suitable Room**: If no exact match is found, the group is allocated to the smallest room that can accommodate the group.
- **Largest Available Room**: If no suitable room is found, the group is allocated to the largest available room.
- **Unallocated**: If members remain unallocated due to insufficient room capacity, they are marked as "Unallocated".

### Output

The allocation results are saved to a CSV file (`uploads/allocation_result.csv`) and returned as a list of dictionaries.

## Example Files

**group_file.csv**:
```
groupid,members,gender
1,10,Boys
2,8,Girls
3,6,Boys and 4 Girls
```

**hostel_file.csv**:
```
hostelname,roomnumber,capacity,gender
HostelA,101,10,Boys
HostelA,102,8,Girls
HostelB,201,6,Boys
HostelB,202,4,Girls
```

## Final Notes

Ensure that the CSV files provided have the correct format and column names. The allocation process depends on accurate data and appropriate gender-specific room availability. If you encounter any issues or need further customization, feel free to modify the code accordingly.
