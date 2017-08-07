## Benchmark Results

### BitVector Library
| Test Description                  | Time           |
| --------------------------------- |:--------------:|
| Random Initialisation (50)        | 0.000141s      |
| Random Initialisation (10,000)    | 0.022201s      |
| Random Initialisation (250,000)   | 0.553810s      |
| Random Initialisation (1,000,000) | 2.177130s      |
| Random Access (50)                | 0.000006s      |
| Random Access (10,000)            | 0.000005s      |
| Random Access (250,000)           | 0.000005s      |
| Random Access (1,000,000)         | 0.000006s      |


### bitarray Library
| Test Description                  | Time           |
| --------------------------------- |:--------------:|
| Random Initialisation (50)        | 0.000007s      |
| Random Initialisation (10,000)    | 0.000643s      |
| Random Initialisation (250,000)   | 0.015690s      |
| Random Initialisation (1,000,000) | 0.065976s      |
| Random Access (50)                | --      |
| Random Access (10,000)            | --      |
| Random Access (250,000)           | --      |
| Random Access (1,000,000)         | --      |

Note: The sizes used for this library were in bytes - Test results need to be updated