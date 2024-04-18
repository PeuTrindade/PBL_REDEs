import { TbAirConditioningDisabled } from "react-icons/tb";
import { FaPowerOff } from "react-icons/fa";
import { FaTemperatureEmpty } from "react-icons/fa6";

function List({ items }) {
    const onClickModeButton = async (address, mode) => {
        try {
            await fetch(`http://127.0.0.1:5000//change_mode/${address}/${mode}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                  }
            });
        } catch (error) {
            console.info(error)
        }
    }

    return (
        <ul class="list-group mt-3">
            {items && items.map((item, key) => {
                return (
                    <li key={key} class="d-flex align-items-center justify-content-between list-group-item">
                        <span style={{ gap: '10px'}} className="d-flex">
                          <TbAirConditioningDisabled fontSize={25} />
                          {item.title}  
                        </span>
                        <span style={{ gap: '10px'}} className="d-flex align-items-center">
                          <FaPowerOff color={item.on ? 'green': 'red'} onClick={() => onClickModeButton(item.title, item.on ? 'off': 'on')} cursor='pointer' fontSize={18} />

                          <span style={{ gap: '1px'}} className="d-flex align-items-center">
                            <FaTemperatureEmpty fontSize={18} />
                            {`${item.temperature}°C`}
                          </span>
                        </span>
                    </li>
                )
            })}
        </ul>
    )
}


export default List;