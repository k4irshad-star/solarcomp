import streamlit as st

# Add custom CSS for dropdown styling
st.markdown(
    """
    <style>
    /* Container for dropdown labels */
    .dropdown-container {
        background-color: #34eb83;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 8px 0;
    }
    
    /* Style the actual dropdown menu when opened */
    .stSelectbox [data-testid="stSelectbox"] div[role="listbox"] {
        background-color: #34eb83 !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin-top: 4px !important;
    }
    
    /* Style the dropdown options */
    .stSelectbox [data-testid="stSelectbox"] div[role="listbox"] div {
        padding: 8px 12px !important;
        border-radius: 4px !important;
        margin: 2px 0 !important;
    }
    
    /* Hover effect for dropdown options */
    .stSelectbox [data-testid="stSelectbox"] div[role="listbox"] div:hover {
        background-color: #e9ecef !important;
    }
    
    /* Style multiselect dropdowns as well */
    .stMultiSelect [data-testid="stMultiSelect"] div[role="listbox"] {
        background-color: #34eb83 !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin-top: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔆 Solar Product Configurator with Inline Component Settings")

# --- Step 1: Product Selection ---
st.subheader("Select a Product")

# Products (main appliances)
products = {
    "Rice Mill": {"base_price": 800, "default_voltage": "AC", "default_rating": 230, "default_power_watts": 1500, "weight": 45},
    "Custom Product": {"base_price": 300, "default_voltage": "DC", "default_rating": 24, "default_power_watts": 500, "weight": 0}
}

selected_product = st.selectbox("Choose a product:", list(products.keys()))
product_info_base = products[selected_product]

# --- Product Configuration ---
st.subheader("Product Configuration")

# Voltage type selection
voltage_type = st.radio(
    "Product Voltage Type:",
    ["DC", "AC"],
    index=0 if product_info_base["default_voltage"] == "DC" else 1,
    key="product_voltage"
)

# Voltage rating based on type
if voltage_type == "DC":
    voltage_rating = st.selectbox(
        "DC Voltage (V):",
        options=[12, 24, 48],
        index=[12, 24, 48].index(product_info_base["default_rating"]) if product_info_base["default_rating"] in [12, 24, 48] else 1,
        key="dc_voltage"
    )
else:  # AC
    voltage_rating = st.selectbox(
        "AC Voltage (V):",
        options=[110, 120, 220, 230, 240],
        index=[110, 120, 220, 230, 240].index(product_info_base["default_rating"]) if product_info_base["default_rating"] in [110, 120, 220, 230, 240] else 3,
        key="ac_voltage"
    )

# Power requirement
power_watts = st.number_input(
    "Product Power Requirement (W):",
    min_value=0,
    value=product_info_base["default_power_watts"],
    step=100,
    key="product_power"
)

# Custom price adjustment for custom products
if selected_product == "Custom Product":
    price_adjustment = st.number_input(
        "Custom Price Adjustment ($):",
        min_value=-200,
        value=0,
        step=50,
        key="price_adjust"
    )
    final_price = product_info_base["base_price"] + price_adjustment
    product_weight = st.number_input(
        "Product Weight (kg):",
        min_value=0.0,
        value=0.0,
        step=0.5,
        key="product_weight"
    )
else:
    final_price = product_info_base["base_price"]
    product_weight = product_info_base["weight"]

# Final product info
product_info = {
    "name": selected_product,
    "price": final_price,
    "voltage": voltage_type,
    "rating": voltage_rating,
    "power_watts": power_watts,
    "weight": product_weight
}

st.markdown(f"**Selected Product:** {product_info['name']}")
st.markdown(f"**Base Price:** ${product_info['price']}")
st.markdown(f"**Specifications:** {product_info['rating']}V {product_info['voltage']}, {product_info['power_watts']}W, {product_info['weight']}kg")

# --- Step 2: Add Components ---
st.markdown("---")
st.subheader("🔌 Add Power System Components")

add_components = st.checkbox("➕ Add power system components (solar, batteries, controllers, etc.)")

# COMPONENTS ONLY (not products) - including all the items from your list
components_data = {
    # Main Products as Components (for power systems)
    "CWS00901 - Auto washer": {"base_price": 350, "weight": 18.0, "category": "Appliances", "default_voltage": "DC", "default_power": 500, "default_rating": 24},
    "CCP00801 - SunPot": {"base_price": 100, "weight": 7.0, "category": "Appliances", "default_voltage": "DC", "default_power": 500, "default_rating": 24},
    "CCA00801 - SunPot auto": {"base_price": 150, "weight": 8.0, "category": "Appliances", "default_voltage": "DC", "default_power": 500, "default_rating": 24},
    "CCP00501 - SolarEPC": {"base_price": 50, "weight": 6.0, "category": "Appliances", "default_voltage": "DC", "default_power": 500, "default_rating": 24},
    "CMM75001 - Mighty Motor 750W": {"base_price": 300, "weight": 11.0, "category": "Appliances", "default_voltage": "DC", "default_power": 750, "default_rating": 24},
    "CIM00501 - Ice-maker 50kg": {"base_price": 1300, "weight": 40.0, "category": "Appliances", "default_voltage": "DC", "default_power": 180, "default_rating": 24},
    
    # Solar Controllers
    "CSC04001 - Controller Pod": {"base_price": 150, "weight": 2.0, "category": "Controllers", "power_rating": 960, "voltage": "DC", "max_current": 40, "default_rating": 24},
    "CSC48401 - Controller Beast": {"base_price": 120, "weight": 0.5, "category": "Controllers", "power_rating": 1920, "voltage": "DC", "max_current": 40, "default_rating": 48},
    
    # Batteries
    # Batteries
"CBA75001 - Battery 750Wh": {
    "base_price": 150, 
    "weight": 9.0, 
    "category": "Batteries", 
    "voltage": 24, 
    "capacity_ah": 15, 
    "charge_c_rating": 1.0,  # NEW
    "discharge_c_rating": 2.0,  # NEW
    "default_rating": 24
},
"CBA15001 - Battery 1.5kWh": {
    "base_price": 250, 
    "weight": 18.0, 
    "category": "Batteries", 
    "voltage": 24, 
    "capacity_ah": 30, 
    "charge_c_rating": 1.0,  # NEW
    "discharge_c_rating": 2.0,  # NEW
    "default_rating": 24
},
"CBA20001 - Battery 5kWh": {
    "base_price": 1000, 
    "weight": 50.0, 
    "category": "Batteries", 
    "voltage": 24.0, 
    "capacity_ah": 100, 
    "charge_c_rating": 1.0,  # NEW
    "discharge_c_rating": 2.0,  # NEW
    "includes_controller": True, 
    "default_rating": 24
},    
"Custom Battery": {
    "base_price": 100, 
    "weight": 10.0, 
    "category": "Batteries", 
    "voltage": 24, 
    "capacity_ah": 0, 
    "charge_c_rating": 1.0,  # NEW
    "discharge_c_rating": 2.0,  # NEW
    "default_rating": 24
},
    # Power Conversion
    
        # Power Conversion
    "Inverter": {
        "base_price": 200, 
        "weight": 2.0, 
        "category": "Power Conversion", 
        "voltage": "DC → AC", 
        "dc_input_voltage": 48,
        "capacity_options": [
            {"capacity": 500, "price_adjust": 0},
            {"capacity": 1000, "price_adjust": 100},
            {"capacity": 2000, "price_adjust": 300},
            {"capacity": 3000, "price_adjust": 500},
            {"capacity": 5000, "price_adjust": 800}
        ]
    },
    
    # Solar Inverter (All-in-one unit)
    "Solar Inverter": {
        "base_price": 500, 
        "weight": 5.0, 
        "category": "Power Conversion", 
        "voltage": "All-in-one", 
        "dc_input_voltage": 48,
        "capacity_options": [
            {"capacity": 3000, "price_adjust": 0},
            {"capacity": 5000, "price_adjust": 300},
            {"capacity": 8000, "price_adjust": 600},
            {"capacity": 10000, "price_adjust": 1000}
        ],
        "is_solar_inverter": True, 
        "includes_mppt": True
    },

    # Solar Panels
    "CSP12501 - Solar panel 125W": {"base_price": 45, "weight": 8.0, "category": "Solar Panels", "power_rating": 125, "voltage": 24, "default_rating": 24},
    "CSP32501 - Solar panel 325W": {"base_price": 75, "weight": 20.0, "category": "Solar Panels", "power_rating": 325, "voltage": 24, "default_rating": 24},
    "CSP50001 - Solar panel 500W": {"base_price": 90, "weight": 8.0, "category": "Solar Panels", "power_rating": 500, "voltage": 24, "default_rating": 24},
    "CSP25001 - Solar panel 250Wp": {"base_price": 50, "weight": 15.0, "category": "Solar Panels", "power_rating": 250, "voltage": 24, "default_rating": 24},
    
    # Cables & Mounting
    "CSR12501 - Rail mount kit 125/250": {"base_price": 16, "weight": 1.5, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSY00101 - Y-splitter, male 2.5-6": {"base_price": 10, "weight": 0.1, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSY00201 - Y-splitter, female 2.5-6": {"base_price": 10, "weight": 0.1, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSC00506 - Solar cable 2.5mm, 5m": {"base_price": 16, "weight": 1.5, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSC01006 - Solar cable 2.5mm, 10m": {"base_price": 32, "weight": 3.0, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSC00506 - Solar cable 4mm, 5m": {"base_price": 20, "weight": 2.0, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSC01006 - Solar cable 4mm, 10m": {"base_price": 40, "weight": 4.0, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSC00506 - Solar cable 6mm, 5m": {"base_price": 24, "weight": 2.5, "category": "Cables & Mounting", "voltage": "N/A"},
    "CSC01006 - Solar cable 6mm, 10m": {"base_price": 48, "weight": 5.0, "category": "Cables & Mounting", "voltage": "N/A"},
    "CBC00201 - Battery cable, 3m x 16mm": {"base_price": 48, "weight": 1.5, "category": "Cables & Mounting", "voltage": "N/A"},
    "CLC00201 - Load cable, 3m x 16mm": {"base_price": 70, "weight": 1.5, "category": "Cables & Mounting", "voltage": "N/A"},
    "CCC00101 - Conversion cable for cookpot": {"base_price": 5, "weight": 0.1, "category": "Cables & Mounting", "voltage": "N/A"},
    "CCC00201 - Conversion cable for battery-to-load": {"base_price": 5, "weight": 0.2, "category": "Cables & Mounting", "voltage": "N/A"},
    
    # Insulated Boxes
    "CIB00901 - VIP 90L icebox": {"base_price": 180, "weight": 10.0, "category": "Accessories", "voltage": "N/A"},
    
    # Cooker Accessories
    "CCP00001 - Spare pot 6L": {"base_price": 7, "weight": 0.5, "category": "Cooker Accessories", "voltage": "N/A"},
    "CCP00002 - Spare pot 5L": {"base_price": 7, "weight": 0.5, "category": "Cooker Accessories", "voltage": "N/A"},
    "CCS00001 - Small steamer": {"base_price": 5, "weight": 0.2, "category": "Cooker Accessories", "voltage": "N/A"},
    "CCS00002 - Big steamer": {"base_price": 10, "weight": 0.4, "category": "Cooker Accessories", "voltage": "N/A"},
    "CCB00001 - Pot bag": {"base_price": 7, "weight": 0.2, "category": "Cooker Accessories", "voltage": "N/A"},
    
    # Motor Attachments
    "CGB00101 - Gearbox": {"base_price": 300, "weight": 5.0, "category": "Motor Attachments", "voltage": "DC", "default_rating": 24},
    "COE00001 - Oil expeller": {"base_price": 300, "weight": 6.0, "category": "Motor Attachments", "voltage": "DC", "default_rating": 24},
    "CME02201 - Meat mincer": {"base_price": 100, "weight": 5.0, "category": "Motor Attachments", "voltage": "DC", "default_rating": 24},
    "CFG00001 - Flour grinder": {"base_price": 300, "weight": 3.0, "category": "Motor Attachments", "voltage": "DC", "default_rating": 24},
    "CVG00001 - Veg grater": {"base_price": 250, "weight": 3.0, "category": "Motor Attachments", "voltage": "DC", "default_rating": 24},
    "CRH00101 - Rice huller": {"base_price": 850, "weight": 15.0, "category": "Motor Attachments", "voltage": "DC", "default_rating": 24},
    "CRP00101 - Rice polisher": {"base_price": 300, "weight": 35.0, "category": "Motor Attachments", "voltage": "DC", "default_rating": 24},
}

user_components = []
total_component_cost = 0
total_component_weight = 0

if add_components:
    st.subheader("Select Components to Include")
    
    selected_controller = None  # Track which controller is selected
    selected_inverter = None    # ADD THIS: Track which inverter is selected

    # Group components by category
    categories = sorted(set(comp_data["category"] for comp_data in components_data.values()))
    
    for category in categories:
        st.markdown(f"**{category}**")
        category_components = {name: data for name, data in components_data.items() if data["category"] == category}

                # ADD THESE 2 LINES HERE (for Controllers category only):
        if category == "Controllers":
            selected_controller = st.radio("Select a Controller:", ["None"] + list(category_components.keys()))
        
        # ADD THIS: For Power Conversion (Inverters) category
        if category == "Power Conversion":
            selected_inverter = st.radio("Select an Inverter:", ["None", "Inverter", "Solar Inverter"])        


        for name, comp_data in category_components.items():
                        # REPLACE THIS LINE:
            # Determine if component is checked
            if category == "Controllers":
                checked = (selected_controller == name)
            elif category == "Power Conversion":  # ADD THIS
                checked = (selected_inverter == name)
            else:
                checked = st.checkbox(name, key=f"check_{name}")

            # ADD THIS NEW CHECK:
            if checked and category == "Controllers" and selected_controller == "None":
                checked = False  # Don't show settings if "None" is selected
            
             # ADD THIS CHECK for Inverters:
            if checked and category == "Power Conversion" and selected_inverter == "None":
                checked = False  # Don't show settings if "None" is selected

            if checked:
                st.markdown(f"**{name} Settings:**")
                
                # Price Input with base price as default
                price = st.number_input(
                    f"💲 {name} Price ($):", 
                    min_value=0, 
                    value=comp_data["base_price"], 
                    step=5, 
                    key=f"price_{name}"
                )

                # Quantity Input for ALL components
                quantity = st.number_input(
                    f"🔢 {name} Quantity:", 
                    min_value=1, 
                    value=1, 
                    step=1, 
                    key=f"qty_{name}"
                )

                # Power Rating for controllers, solar panels, and appliances
                power_rating = comp_data.get("power_rating", 0)
                if power_rating == 0 and "default_power" in comp_data:
                    power_rating = comp_data["default_power"]

                # Inverter Capacity Selection
                # Inverter Capacity Selection
                if name == "Inverter" or name == "Solar Inverter":
                    inverter_option = st.selectbox(
                        "Inverter Capacity:",
                        options=comp_data["capacity_options"],
                        format_func=lambda x: f"{x['capacity']}W",
                        key=f"inverter_cap_{name}"
                    )
                    power_rating = inverter_option["capacity"]
                    price += inverter_option["price_adjust"]
                    st.markdown(f"_Capacity: {power_rating}W_")
                    
                    # Add special note for Solar Inverter
                    if name == "Solar Inverter":
                        st.markdown("_All-in-one unit: Solar → Battery → AC (includes MPPT controller)_")
                
                if power_rating > 0:
                    if "Solar panel" in name:
                        st.markdown(f"_Power Rating: {power_rating}Wp_")
                    else:
                        st.markdown(f"_Power Rating: {power_rating}W_")
                
                # Current rating for controllers
                max_current = comp_data.get("max_current", 0)
                if max_current > 0:
                    st.markdown(f"_Max Current: {max_current}A_")
                
                # Define battery_capacity_wh with default value for ALL components
                battery_capacity_wh = 0
                battery_capacity_ah = 0
                battery_voltage = 24
                battery_charge_c_rating = 1.0  # CHANGE THIS
                battery_discharge_c_rating = 1.0  # ADD THIS 
                #new changes
                # Battery Specific Settings


                # Battery Specific Settings
                if "Battery" in name:
                    battery_capacity_ah = comp_data.get("capacity_ah", 0)
                    battery_voltage = comp_data.get("voltage", 24)
                    battery_charge_c_rating = comp_data.get("charge_c_rating", 1.0)  # NEW
                    battery_discharge_c_rating = comp_data.get("discharge_c_rating", 1.0)  # NEW
                    
                    if battery_capacity_ah > 0:
                        # Pre-configured battery - show Ah and calculated Wh
                        battery_capacity_wh = battery_voltage * battery_capacity_ah
                        st.markdown(f"_Capacity: {battery_capacity_ah}Ah ({battery_capacity_wh}Wh), Voltage: {battery_voltage}V_")
                    else:
                        # Custom battery - allow user to input Ah and Voltage
                        battery_capacity_ah = st.number_input(
                            "🔋 Battery Capacity (Ah):", 
                            min_value=0, 
                            value=100, 
                            step=10, 
                            key=f"capacity_ah_{name}"
                        )
                        battery_voltage = st.number_input(
                            "⚡ Battery Voltage (V):",
                            min_value=0,
                            value=24,
                            step=12,
                            key=f"batt_volt_{name}"
                        )
                        battery_capacity_wh = battery_voltage * battery_capacity_ah
                    
                    # Charge C-Rating dropdown
                    st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
                    battery_charge_c_rating = st.selectbox(
                        "Charge C-Rating (input from solar):", 
                        options=[0.5, 1.0, 2.0, 3.0], 
                        index=[0.5, 1.0, 2.0, 3.0].index(battery_charge_c_rating) if battery_charge_c_rating in [0.5, 1.0, 2.0, 3.0] else 1,
                        key=f"charge_crate_{name}"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Discharge C-Rating dropdown
                    st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
                    battery_discharge_c_rating = st.selectbox(
                        "Discharge C-Rating (output to loads):", 
                        options=[0.5, 1.0, 2.0, 3.0], 
                        index=[0.5, 1.0, 2.0, 3.0].index(battery_discharge_c_rating) if battery_discharge_c_rating in [0.5, 1.0, 2.0, 3.0] else 1,
                        key=f"discharge_crate_{name}"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display max charge/discharge power
                    max_charge_power = battery_capacity_wh * battery_charge_c_rating
                    max_discharge_power = battery_capacity_wh * battery_discharge_c_rating
                    st.markdown(f"_Max solar input: {max_charge_power:.0f}W_")
                    st.markdown(f"_Max load output: {max_discharge_power:.0f}W_")
                # Auto-assign voltage type
                # Auto-assign voltage type
                                # Auto-assign voltage type
                voltage_type = comp_data.get("voltage", "DC")
                if "Battery" in name:
                    st.markdown("_Voltage Type: DC (fixed for batteries)_")
                elif name == "Inverter":
                    dc_voltage = comp_data.get("default_rating", 48)  # or dc_input_voltage if you renamed it
                    st.markdown(f"_Converts DC to AC (DC input: {dc_voltage}V, AC output: {voltage_rating}V)_")
                elif name == "Solar Inverter":
                    dc_voltage = comp_data.get("default_rating", 48)  # or dc_input_voltage if you renamed it
                    st.markdown(f"_All-in-one: Solar → Battery → AC (DC input: {dc_voltage}V, includes MPPT)_")

                # Voltage Input for configurable components - FIXED HERE
                voltage_value = comp_data.get("default_rating", 24)
                
                if "Controller" in name and "Beast" not in name:
                    st.markdown("Select supported input voltages:")
                    voltage_inputs = st.multiselect(
                        "Supported Voltages (V):",
                        options=[12, 24, 48],
                        default=[12, 24],
                        key=f"volt_multi_{name}"
                    )
                    voltage_value = ", ".join(str(v) for v in voltage_inputs)
                elif voltage_type != "N/A" and "Battery" not in name and name != "Inverter" and "Solar panel" not in name and "default_voltage" not in comp_data:
                    # Ensure voltage_value is an integer for number_input
                    if isinstance(voltage_value, str):
                        try:
                            voltage_value = int(voltage_value)
                        except ValueError:
                            voltage_value = 24
                    
                    voltage_value = st.number_input(
                        f"{name} Voltage (V):", 
                        min_value=0, 
                        value=int(voltage_value),  # Convert to int
                        step=12, 
                        key=f"volt_{name}"
                    )
                elif "default_rating" in comp_data:
                    voltage_value = comp_data["default_rating"]

                # Weight display
                component_weight = comp_data["weight"]
                st.markdown(f"_Weight: {component_weight}kg_")

                # Add to component list
                # Add to component list
                for i in range(quantity):
                    user_components.append({
                        "name": name,
                        "price": price,
                        "voltage": voltage_type,
                        "rating": voltage_value,
                        "power_rating": power_rating,
                        "max_current": max_current,
                        "battery_capacity": battery_capacity_wh,
                        "battery_capacity_ah": battery_capacity_ah,
                        "battery_voltage": battery_voltage,
                        "battery_charge_c_rating": battery_charge_c_rating,  # NEW - ADD THIS
                        "battery_discharge_c_rating": battery_discharge_c_rating,  # NEW - ADD THIS
                        # "battery_c_rating": battery_c_rating,  # REMOVE OR COMMENT THIS LINE
                        "weight": component_weight,
                        "category": comp_data["category"],
                        "includes_controller": comp_data.get("includes_controller", False),
                        "includes_mppt": comp_data.get("includes_mppt", False),  # NEW
                        "is_solar_inverter": comp_data.get("is_solar_inverter", False),  # NEW
                        "is_appliance": "Appliances" in comp_data["category"],
                        "quantity": quantity
                    })
                    total_component_cost += price
                    total_component_weight += component_weight

# --- Step 3: Summary ---
st.markdown("---")
st.subheader("🧾 Configuration Summary")

st.write(f"**Selected Product:** {product_info['name']}")
st.write(f"**Product Specifications:** {product_info['rating']}V {product_info['voltage']}, {product_info['power_watts']}W")
st.write(f"**Product Weight:** {product_info['weight']}kg")
st.write(f"**Product Price:** ${product_info['price']}")

if user_components:
    st.write("**Added Components:**")
    components_by_category = {}
    for comp in user_components:
        category = comp.get('category', 'Other')
        if category not in components_by_category:
            components_by_category[category] = []
        components_by_category[category].append(comp)
    
    for category, comps in components_by_category.items():
        st.markdown(f"**{category}:**")
        for c in comps:
            quantity = c.get('quantity', 1)
            if "Battery" in c['name']:
                battery_charge_c = c.get('battery_charge_c_rating', 1.0)
                battery_discharge_c = c.get('battery_discharge_c_rating', 1.0)
                if quantity > 1:
                    st.markdown(f"- {c['name']} — ${c['price']} each × {quantity} = ${c['price'] * quantity} ({c['rating']}V, {c['battery_capacity_ah']}Ah, Charge: {battery_charge_c}C/Discharge: {battery_discharge_c}C, {c['weight']}kg each)")
                else:
                    st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V, {c['battery_capacity_ah']}Ah, Charge: {battery_charge_c}C/Discharge: {battery_discharge_c}C, {c['weight']}kg)")
            elif "Controller" in c['name']:
                if quantity > 1:
                    st.markdown(f"- {c['name']} — ${c['price']} each × {quantity} = ${c['price'] * quantity} ({c['rating']}V, {c['power_rating']}W, {c['max_current']}A, {c['weight']}kg each)")
                else:
                    st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V, {c['power_rating']}W, {c['max_current']}A, {c['weight']}kg)")
            elif "Solar panel" in c['name']:
                if quantity > 1:
                    st.markdown(f"- {c['name']} — ${c['price']} each × {quantity} = ${c['price'] * quantity} ({c['rating']}V, {c['power_rating']}Wp, {c['weight']}kg each)")
                else:
                    st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V, {c['power_rating']}Wp, {c['weight']}kg)")
            elif c['name'] == "Inverter":
                if quantity > 1:
                    st.markdown(f"- {c['name']} — ${c['price']} each × {quantity} = ${c['price'] * quantity} ({c['voltage']}, {c['weight']}kg each)")
                else:
                    st.markdown(f"- {c['name']} — ${c['price']} ({c['voltage']}, {c['weight']}kg)")
            elif c.get('is_appliance', False):
                if quantity > 1:
                    st.markdown(f"- {c['name']} — ${c['price']} each × {quantity} = ${c['price'] * quantity} ({c['rating']}V {c['voltage']}, {c['power_rating']}W, {c['weight']}kg each)")
                else:
                    st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V {c['voltage']}, {c['power_rating']}W, {c['weight']}kg)")
            else:
                if quantity > 1:
                    st.markdown(f"- {c['name']} — ${c['price']} each × {quantity} = ${c['price'] * quantity} ({c.get('voltage', 'N/A')}, {c['weight']}kg each)")
                else:
                    st.markdown(f"- {c['name']} — ${c['price']} ({c.get('voltage', 'N/A')}, {c['weight']}kg)")
else:
    st.write("No components added.")

total_cost = product_info["price"] + total_component_cost
total_weight = product_info["weight"] + total_component_weight

st.markdown(f"### 💰 Total System Cost: ${total_cost}")
st.markdown(f"### ⚖️ Total System Weight: {total_weight}kg")

# --- Step 4: Engineering Viability Check ---
#st.markdown("---")
#st.subheader("⚙️ Engineering Compatibility Check1")

viable = True
messages = []

# Get component types for easier checking
has_battery = any("Battery" in c["name"] for c in user_components)
has_inverter = any(c["name"] == "Inverter" for c in user_components)
has_solar_inverter = any(c["name"] == "Solar Inverter" for c in user_components)  # NEW
has_controller = any("Controller" in c["name"] for c in user_components)
has_solar_panels = any("Solar panel" in c["name"] for c in user_components)
has_appliances = any(c.get("is_appliance", False) for c in user_components)

appliances = [c for c in user_components if c.get("is_appliance", False)]

batteries = [c for c in user_components if "Battery" in c["name"]]
controllers = [c for c in user_components if "Controller" in c["name"]]
solar_panels = [c for c in user_components if "Solar panel" in c["name"]]
inverter = next((c for c in user_components if c["name"] == "Inverter"), None)
solar_inverter = next((c for c in user_components if c["name"] == "Solar Inverter"), None)  # NEW
# Get all AC loads (product + AC appliances)
all_ac_loads = []

# Add main product if it's AC
if product_info["voltage"] == "AC":
    all_ac_loads.append({
        "name": product_info["name"],
        "power": product_info["power_watts"]
    })

# Add AC appliances from components
for appliance in appliances:
    if appliance.get("voltage") == "AC":
        all_ac_loads.append({
            "name": appliance["name"],
            "power": appliance.get("power_rating", 0)
        })

# Find the biggest single AC load
biggest_ac_load_power = 0
biggest_ac_load_name = ""
for load in all_ac_loads:
    if load["power"] > biggest_ac_load_power:
        biggest_ac_load_power = load["power"]
        biggest_ac_load_name = load["name"]

# Calculate total AC load power
total_ac_load_power = sum(load["power"] for load in all_ac_loads)
motor_attachments = [c for c in user_components if c["category"] == "Motor Attachments"]
cooker_accessories = [c for c in user_components if c["category"] == "Cooker Accessories"]
#appliances = [c for c in user_components if c.get("is_appliance", False)]
iceboxes = [c for c in user_components if "icebox" in c["name"].lower()]

# --- System Status Helper Function ---
def get_system_status(has_battery, has_inverter, has_solar_inverter, has_solar_panels, has_controller, batteries):
    """Determine system status based on component selection"""
    
    # Red: Electrically impossible
    if not has_battery and not has_solar_panels and not has_solar_inverter:
        return "red", "❌ No energy source (needs battery, solar panels, or solar inverter)"
    
    # Green: Complete solar system with Solar Inverter
    if has_solar_inverter and has_battery:
        return "green", "✅ Complete solar system with Solar Inverter (all-in-one unit)"
    
    # Green: Complete solar system with traditional setup
    if has_solar_panels and has_battery:
        # Check if we have a controller or battery with built-in controller
        battery_has_controller = any(b.get("includes_controller", False) for b in batteries if "Battery" in b["name"])
        if has_controller or battery_has_controller:
            return "green", "✅ Complete solar system with energy source and storage"
    
    # Orange: Works conditionally (missing solar panels but has battery+inverter)
    if has_battery and has_inverter and not has_solar_panels and not has_solar_inverter:
        return "orange", "⚠️ System will work but needs external energy source (grid/generator) or user-provided solar panels"
    
    # Orange: Solar Inverter without battery
    if has_solar_inverter and not has_battery:
        return "orange", "⚠️ Solar Inverter needs a battery for energy storage"
    
    # Orange: Traditional system without controller
    if has_battery and not has_solar_inverter:
        return "orange", "⚠️ System has storage but may need additional components for complete operation"
    
    return "red", "❌ Incomplete system configuration"

# --- Rule 1: AC Product with DC Components requires Inverter ---
# --- Rule 1: AC Product with DC Components requires Inverter ---
if product_info["voltage"] == "AC" and (has_battery or has_appliances) and not has_inverter and not has_solar_inverter:
    viable = False
    messages.append("⚠️ AC product requires either Inverter or Solar Inverter when using DC components like Battery or DC appliances")


# --- Rule 2: DC Product should not use Inverter ---
if product_info["voltage"] == "DC" and has_inverter:
    viable = False
    messages.append("⚠️ DC product cannot use Inverter (already DC-compatible)")

# --- Rule 3: Battery requires compatible Controller (unless battery includes one) ---
# BUT only check this if we have solar panels
if has_battery and has_solar_panels and not has_controller:
    battery_with_controller = any(b.get("includes_controller", False) for b in batteries)
    if not battery_with_controller:
        viable = False
        messages.append("⚠️ Solar panels require a Solar Controller when connected to a battery")

# --- Rule 4: Voltage matching between Battery and Controllers ---
for battery in batteries:
    for controller in controllers:
        if controller.get("includes_controller", False):
            continue  # Skip if controller is included with battery
            
        try:
            if "Beast" in controller["name"]:
                # Controller Beast is 48V specific
                battery_rating = float(battery["rating"]) if isinstance(battery["rating"], (int, float, str)) else 0
                if battery_rating != 51.2:
                    viable = False
                    messages.append(f"⚠️ {battery['name']} ({battery['rating']}V) not compatible with {controller['name']} (48V system only)")
            else:
                # Other controllers support multiple voltages
                if isinstance(controller["rating"], str):
                    controller_voltages = [int(v.strip()) for v in str(controller["rating"]).split(",")]
                else:
                    controller_voltages = [int(controller["rating"])]
                
                battery_rating = int(battery["rating"]) if isinstance(battery["rating"], (int, float, str)) else 0
                if battery_rating not in controller_voltages:
                    viable = False
                    messages.append(f"⚠️ {battery['name']} ({battery['rating']}V) not compatible with {controller['name']} (supports {controller['rating']}V)")
        except (ValueError, AttributeError):
            viable = False
            messages.append(f"⚠️ Invalid voltage configuration between {battery['name']} and {controller['name']}")


# --- Rule 4.5: Voltage matching between Battery and Inverters ---
for battery in batteries:
    battery_rating = battery["rating"]
    
    # Check with Plain Inverter
    if inverter:
        try:
            # Inverters have a default_rating for their DC input voltage
            inverter_rating = int(inverter.get("rating", 0))
            if battery_rating != inverter_rating:
                viable = False
                messages.append(f"⚠️ {battery['name']} ({battery_rating}V) not compatible with {inverter['name']} DC input ({inverter_rating}V)")
        except (ValueError, TypeError):
            viable = False
            messages.append(f"⚠️ Voltage configuration error between {battery['name']} and {inverter['name']}")
    
    # Check with Solar Inverter
    if solar_inverter:
        try:
            # Solar Inverters also have a default_rating for DC input
            solar_inverter_rating = int(solar_inverter.get("rating", 0))
            if battery_rating != solar_inverter_rating:
                viable = False
                messages.append(f"⚠️ {battery['name']} ({battery_rating}V) not compatible with {solar_inverter['name']} DC input ({solar_inverter_rating}V)")
        except (ValueError, TypeError):
            viable = False
            messages.append(f"⚠️ Voltage configuration error between {battery['name']} and {solar_inverter['name']}")


# --- Rule 5: Total power calculation for appliances ---
total_appliance_power = sum(float(appliance.get("power_rating", 0)) for appliance in appliances) + product_info["power_watts"]
if has_controller:
    for controller in controllers:
        controller_power = float(controller.get("power_rating", 0))
        if total_appliance_power > controller_power:
            viable = False
            messages.append(f"⚠️ Total appliance power ({total_appliance_power}W) exceeds {controller['name']} max output ({controller_power}W)")

# --- Rule 6: Battery C-rating limits ---
# --- Rule 6: Battery Charge/Discharge C-rating limits ---
for battery in batteries:
    battery_capacity = float(battery.get("battery_capacity", 0))
    battery_charge_c_rating = float(battery.get("battery_charge_c_rating", 1.0))
    battery_discharge_c_rating = float(battery.get("battery_discharge_c_rating", 1.0))
    
    max_charge_power = battery_capacity * battery_charge_c_rating
    max_discharge_power = battery_capacity * battery_discharge_c_rating
    
    # Check if solar power exceeds battery charge rating
    if solar_panels:
        total_solar_power = sum(float(panel.get("power_rating", 0)) for panel in solar_panels)
        if total_solar_power > max_charge_power:
            viable = False
            messages.append(f"⚠️ Total solar power ({total_solar_power}W) exceeds {battery['name']} max charge rate ({max_charge_power:.0f}W)")
    
    # Check if total load exceeds battery discharge rating
    if total_appliance_power > max_discharge_power:
        viable = False
        messages.append(f"⚠️ Total load ({total_appliance_power}W) exceeds {battery['name']} max discharge rate ({max_discharge_power:.0f}W)")
# --- Rule 7: Motor attachment compatibility ---
if motor_attachments and not any("Mighty Motor" in appliance["name"] for appliance in appliances):
    viable = False
    messages.append("⚠️ Motor attachments require a Mighty Motor appliance in the system")

# --- Rule 8: Cooker accessories compatibility ---
if cooker_accessories and not any("SunPot" in appliance["name"] or "SolarEPC" in appliance["name"] for appliance in appliances):
    viable = False
    messages.append("⚠️ Cooker accessories require a SunPot or SolarEPC appliance in the system")

# --- Rule 9: Solar panel compatibility ---
if solar_panels and controllers:
    total_solar_power = sum(float(panel.get("power_rating", 0)) for panel in solar_panels)
    for controller in controllers:
        controller_power = float(controller.get("power_rating", 0))
        if total_solar_power > controller_power:
            viable = False
            messages.append(f"⚠️ Total solar panel power ({total_solar_power}W) exceeds {controller['name']} max input ({controller_power}W)")

# --- Rule 10: Ice-maker and icebox compatibility ---
if any("Ice-maker" in appliance["name"] for appliance in appliances) and not iceboxes:
    st.warning("💡 Consider adding an insulated icebox for optimal ice-maker performance")

# --- Rule 11: Inverter capacity check ---
if inverter and all_ac_loads:
    inverter_power = float(inverter.get("power_rating", 0))
    
    # Check if inverter can handle the biggest single load
    if biggest_ac_load_power > inverter_power:
        viable = False
        messages.append(f"⚠️ {biggest_ac_load_name} ({biggest_ac_load_power}W) exceeds Inverter capacity ({inverter_power}W)")
    
    # Show info about total AC load (not an error, just information)
    if len(all_ac_loads) > 1:
        messages.append(f"ℹ️ Total AC load: {total_ac_load_power}W (across {len(all_ac_loads)} devices)")


# --- Rule 12: System configuration compatibility ---
# Check if system uses allowed combinations
if has_solar_inverter:
    # Solar Inverter systems
    if has_inverter:
        viable = False
        messages.append("⚠️ Solar Inverter cannot be used with a plain Inverter (redundant)")
    
    if has_controller and not any(b.get("includes_controller", False) for b in batteries):
        messages.append("ℹ️ Note: Solar Inverter includes built-in MPPT controller")
    
    if not has_battery:
        viable = False
        messages.append("⚠️ Solar Inverter requires a battery for energy storage")
    
    # Check if Solar Inverter has enough capacity
    if solar_inverter and all_ac_loads:
        solar_inverter_power = float(solar_inverter.get("power_rating", 0))
        if biggest_ac_load_power > solar_inverter_power:
            viable = False
            messages.append(f"⚠️ {biggest_ac_load_name} ({biggest_ac_load_power}W) exceeds Solar Inverter capacity ({solar_inverter_power}W)")
else:
    # Traditional systems
    # Traditional systems
    if product_info["voltage"] == "AC" and has_battery and not has_inverter and not has_solar_inverter:
        viable = False
        messages.append("⚠️ AC system requires either Inverter or Solar Inverter with battery") 


    if has_solar_panels and has_battery and not has_controller and not any(b.get("includes_controller", False) for b in batteries):
        viable = False
        messages.append("⚠️ Solar panels with battery require a Solar Controller")


# --- Step 5: System Status Display ---
st.markdown("---")
st.subheader("🔋 System Status Check")

if user_components:
    # Determine system status
    # Determine system status
    status_color, status_message = get_system_status(
        has_battery, 
        has_inverter, 
        has_solar_inverter,  # ADD THIS
        has_solar_panels, 
        has_controller,
        batteries
    )
    
    # Display status with appropriate color
    if status_color == "green":
        st.success(status_message)
    elif status_color == "orange":
        st.warning(status_message)
    else:  # red
        st.error(status_message)
    
    # --- Engineering Compatibility Check ---
    st.subheader("⚙️ Engineering Compatibility Check")
    
    if not viable:
        st.error("❌ Incompatible system configuration detected:")
        for msg in messages:
            st.markdown(f"- {msg}")
    else:
        st.success("✅ System components are electrically compatible.")
        
else:
    st.info("ℹ️ Add components to check system status and compatibility")



# --- Additional System Summary ---
if user_components:
    st.markdown("---")
    st.subheader("📊 Power System Summary")

    # === ADD THIS NEW CODE BLOCK HERE ===
    # Add energy source indicator
    energy_status = []
    if has_solar_panels:
        energy_status.append("✅ Solar panels")
    if has_battery:
        energy_status.append("✅ Battery storage")
    
    if energy_status:
        st.write("**Energy Configuration:** " + " + ".join(energy_status))
    else:
        st.warning("⚠️ **No energy sources configured**")
    
    st.markdown("")  # Add spacing
    # === END OF NEW CODE ===

    # === NEW: Add inverter and load information ===
    # Add inverter and load information
    if inverter or solar_inverter:
        selected_inverter = inverter if inverter else solar_inverter
        inverter_type = "Solar Inverter" if solar_inverter else "Inverter"
        inverter_power = float(selected_inverter.get("power_rating", 0))
        
        st.write(f"**{inverter_type} Capacity:** {inverter_power}W")
        
        if solar_inverter:
            st.write(f"**Type:** All-in-one (Solar → Battery → AC, includes MPPT)")
        
        if all_ac_loads:
            st.write(f"**Biggest AC Load:** {biggest_ac_load_name} ({biggest_ac_load_power}W)")
            st.write(f"**Total AC Load:** {total_ac_load_power}W")
            
            # Calculate inverter utilization
            if biggest_ac_load_power > 0:
                utilization = (biggest_ac_load_power / inverter_power) * 100
                if utilization <= 100:
                    st.write(f"**{inverter_type} Utilization:** {utilization:.1f}% of capacity")
                else:
                    st.warning(f"⚠️ **{inverter_type} Overload:** {utilization:.1f}% over capacity")
    
    st.markdown("")  # Add spacing
    # === END OF NEW CODE ===
    
    system_limits = {}
    
    system_limits = {}
    
    if solar_panels:
        total_solar_power = sum(float(panel.get("power_rating", 0)) for panel in solar_panels)
        system_limits["Total Solar Power"] = f"{total_solar_power}Wp"
    
    if controllers:
        total_controller_power = sum(float(c.get("power_rating", 0)) for c in controllers)
        system_limits["Total Controller Capacity"] = f"{total_controller_power}W"
    
    if batteries:
        total_battery_capacity = sum(float(b.get("battery_capacity", 0)) for b in batteries)
        
        # Calculate max charge and discharge power
        max_charge_power = sum(float(b.get("battery_capacity", 0)) * float(b.get("battery_charge_c_rating", 1.0)) for b in batteries)
        max_discharge_power = sum(float(b.get("battery_capacity", 0)) * float(b.get("battery_discharge_c_rating", 1.0)) for b in batteries)
        
        system_limits["Total Battery Capacity"] = f"{total_battery_capacity}Wh"
        system_limits["Battery Voltage"] = f"{batteries[0]['rating']}V"  # ADD THIS - assumes all batteries same voltage
        system_limits["Max Solar Input"] = f"{max_charge_power:.0f}W"
        system_limits["Max Load Output"] = f"{max_discharge_power:.0f}W"
    
    if appliances:
        total_appliance_power = sum(float(appliance.get("power_rating", 0)) for appliance in appliances)
        system_limits["Total Appliance Power"] = f"{total_appliance_power}W"
    
    if system_limits:
        for limit, value in system_limits.items():
            st.write(f"**{limit}:** {value}")
    
    st.write(f"**Main Product Power:** {product_info['power_watts']}W")
    st.write(f"**Total System Load:** {total_appliance_power}W")
    
    # Power utilization calculations
    if controllers:
        max_controller_power = max([float(c.get("power_rating", 0)) for c in controllers])
        utilization = (total_appliance_power / max_controller_power) * 100
        st.write(f"**Controller Utilization:** {utilization:.1f}%")

# --- Recommendations ---
if user_components:
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
    # Add warning about missing solar panels - NEW CODE
    if has_battery and has_inverter and not has_solar_panels:
        st.warning("⚠️ **Important:** This system has no built-in energy source. It requires either:")
        st.markdown("- User-provided solar panels")
        st.markdown("- Grid connection (not yet modeled)")
        st.markdown("- Generator input (not yet modeled)")
        st.markdown("")  # Add spacing


        # === NEW: Inverter recommendation ===
    if (inverter or solar_inverter) and all_ac_loads:
        selected_inverter = inverter if inverter else solar_inverter
        inverter_type = "Solar Inverter" if solar_inverter else "Inverter"
        inverter_power = float(selected_inverter.get("power_rating", 0))
        
        # Check if inverter is near capacity
        if biggest_ac_load_power > inverter_power * 0.8:  # If load is more than 80% of inverter capacity
            st.info(f"🔌 **{inverter_type} sizing:** Your biggest load ({biggest_ac_load_power}W) uses {biggest_ac_load_power/inverter_power*100:.0f}% of {inverter_type.lower()} capacity ({inverter_power}W). Consider upgrading for safety margin.")
            st.markdown("")  # Add spacing
        
        # Check if multiple devices exceed total inverter capacity
        if len(all_ac_loads) > 1 and total_ac_load_power > inverter_power:
            st.warning(f"⚠️ **Load management needed:** Total AC load ({total_ac_load_power}W) exceeds {inverter_type.lower()} capacity ({inverter_power}W). Devices cannot run simultaneously.")
            st.markdown("")  # Add spacing
    
    # Solar Inverter specific recommendations
    if has_solar_inverter:
        if not has_battery:
            st.error("❌ **Missing battery:** Solar Inverter requires a battery for energy storage")
        elif has_controller and not any(b.get("includes_controller", False) for b in batteries):
            st.info("💡 **Note:** Solar Inverter includes built-in MPPT controller. External controller may not be needed.")
    
    # REST OF YOUR EXISTING RECOMMENDATIONS (unchanged)
    #Commented out to check
    #if inverter and all_ac_loads:
        #inverter_power = float(inverter.get("power_rating", 0))
        
        # Check if inverter is near capacity
        #if biggest_ac_load_power > inverter_power * 0.8:  # If load is more than 80% of inverter capacity
            #st.info(f"🔌 **Inverter sizing:** Your biggest load ({biggest_ac_load_power}W) uses {biggest_ac_load_power/inverter_power*100:.0f}% of inverter capacity ({inverter_power}W). Consider upgrading for safety margin.")
            #st.markdown("")  # Add spacing
        
        # Check if multiple devices exceed total inverter capacity
        #if len(all_ac_loads) > 1 and total_ac_load_power > inverter_power:
            #st.warning("⚠️ **Load management needed:** Total AC load ({total_ac_load_power}W) exceeds inverter capacity ({inverter_power}W). Devices cannot run simultaneously.")
            #st.markdown("")  # Add spacing


    if has_battery and not has_controller and not any(b.get("includes_controller", False) for b in batteries):
        st.info("Consider adding a Solar Controller for better battery charging efficiency")
    
    if has_solar_panels and not has_controller and not has_battery:
        st.info("Solar panels work best with a battery and controller system for energy storage")
    
    if motor_attachments and len(motor_attachments) > 1:
        st.info("Multiple motor attachments selected - ensure they are compatible with each other")
    
    if any("Ice-maker" in appliance["name"] for appliance in appliances) and not iceboxes:
        st.info("Ice-maker works best with an insulated icebox to maintain ice quality")
    
    if total_appliance_power > 0 and has_battery:
        total_battery_capacity = sum(float(b.get("battery_capacity", 0)) for b in batteries)
        runtime_hours = total_battery_capacity / total_appliance_power
        st.info(f"Estimated battery runtime: {runtime_hours:.1f} hours at full load")
    
    # Cable recommendations
    cables_count = len([c for c in user_components if c["category"] == "Cables & Mounting"])
    if solar_panels and cables_count == 0:
        st.info("Consider adding solar cables and mounting hardware for your solar panels")
    
    if batteries and not any("Battery cable" in c["name"] for c in user_components):
        st.info("Consider adding battery cables for proper battery connections")