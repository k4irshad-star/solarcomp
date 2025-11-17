import streamlit as st

st.title("🔆 Solar Product Configurator with Inline Component Settings")

# --- Step 1: Product Selection ---
st.subheader("Select a Product")

# Products (main appliances)
products = {
    "Rice Mill": {"base_price": 800, "default_voltage": "AC", "default_rating": 230, "default_power_watts": 1500, "weight": 0},
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
    "CBA75001 - Battery 750Wh": {"base_price": 150, "weight": 9.0, "category": "Batteries", "capacity": 750, "voltage": 25.6, "c_rating": 1.0, "default_rating": 25.6},
    "CBA15001 - Battery 1.5kWh": {"base_price": 250, "weight": 18.0, "category": "Batteries", "capacity": 1500, "voltage": 51.2, "c_rating": 1.0, "default_rating": 51.2},
    "CBA20001 - Battery 5kWh": {"base_price": 1000, "weight": 50.0, "category": "Batteries", "capacity": 5000, "voltage": 25.6, "c_rating": 1.0, "includes_controller": True, "default_rating": 25.6},
    
    # Power Conversion
    "Inverter": {"base_price": 200, "weight": 2.0, "category": "Power Conversion", "voltage": "DC → AC", "default_rating": 48},
    
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
    
    # Group components by category
    categories = sorted(set(comp_data["category"] for comp_data in components_data.values()))
    
    for category in categories:
        st.markdown(f"**{category}**")
        category_components = {name: data for name, data in components_data.items() if data["category"] == category}
        
        for name, comp_data in category_components.items():
            checked = st.checkbox(name, key=f"check_{name}")
            
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

                # Power Rating for controllers, solar panels, and appliances
                power_rating = comp_data.get("power_rating", 0)
                if power_rating == 0 and "default_power" in comp_data:
                    power_rating = comp_data["default_power"]
                
                if power_rating > 0:
                    if "Solar panel" in name:
                        st.markdown(f"_Power Rating: {power_rating}Wp_")
                    else:
                        st.markdown(f"_Power Rating: {power_rating}W_")
                
                # Current rating for controllers
                max_current = comp_data.get("max_current", 0)
                if max_current > 0:
                    st.markdown(f"_Max Current: {max_current}A_")
                
                # Battery Specific Settings
                battery_capacity = comp_data.get("capacity", 0)
                battery_c_rating = comp_data.get("c_rating", 1.0)
                if "Battery" in name:
                    if battery_capacity > 0:
                        st.markdown(f"_Capacity: {battery_capacity}Wh, Voltage: {comp_data.get('voltage', 24)}V_")
                    else:
                        battery_capacity = st.number_input(
                            "🔋 Battery Capacity (Wh):", 
                            min_value=0, 
                            value=2000, 
                            step=100, 
                            key=f"capacity_{name}"
                        )
                    battery_c_rating = st.selectbox(
                        "C-Rating:", 
                        options=[0.5, 1.0, 2.0, 3.0], 
                        index=[0.5, 1.0, 2.0, 3.0].index(battery_c_rating) if battery_c_rating in [0.5, 1.0, 2.0, 3.0] else 1,
                        key=f"crate_{name}"
                    )
                    st.markdown(f"_Max charge/discharge: {battery_capacity * battery_c_rating:.0f}W_")

                # Auto-assign voltage type
                voltage_type = comp_data.get("voltage", "DC")
                if "Battery" in name:
                    st.markdown("_Voltage Type: DC (fixed for batteries)_")
                elif name == "Inverter":
                    st.markdown("_Converts DC to AC (input DC, output AC)_")
                elif voltage_type == "N/A":
                    st.markdown("_Voltage: Not Applicable_")
                elif "default_voltage" in comp_data:
                    voltage_type = comp_data["default_voltage"]
                    st.markdown(f"_Voltage Type: {voltage_type}_")
                else:
                    st.markdown(f"_Voltage Type: {voltage_type}_")

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
                user_components.append({
                    "name": name,
                    "price": price,
                    "voltage": voltage_type,
                    "rating": voltage_value,
                    "power_rating": power_rating,
                    "max_current": max_current,
                    "battery_capacity": battery_capacity,
                    "battery_c_rating": battery_c_rating,
                    "weight": component_weight,
                    "category": comp_data["category"],
                    "includes_controller": comp_data.get("includes_controller", False),
                    "is_appliance": "Appliances" in comp_data["category"]
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
            if "Battery" in c['name']:
                st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V, {c['battery_capacity']}Wh, {c['battery_c_rating']}C, {c['weight']}kg)")
            elif "Controller" in c['name']:
                st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V, {c['power_rating']}W, {c['max_current']}A, {c['weight']}kg)")
            elif "Solar panel" in c['name']:
                st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V, {c['power_rating']}Wp, {c['weight']}kg)")
            elif c['name'] == "Inverter":
                st.markdown(f"- {c['name']} — ${c['price']} ({c['voltage']}, {c['weight']}kg)")
            elif c.get('is_appliance', False):
                st.markdown(f"- {c['name']} — ${c['price']} ({c['rating']}V {c['voltage']}, {c['power_rating']}W, {c['weight']}kg)")
            else:
                st.markdown(f"- {c['name']} — ${c['price']} ({c.get('voltage', 'N/A')}, {c['weight']}kg)")
else:
    st.write("No components added.")

total_cost = product_info["price"] + total_component_cost
total_weight = product_info["weight"] + total_component_weight

st.markdown(f"### 💰 Total System Cost: ${total_cost}")
st.markdown(f"### ⚖️ Total System Weight: {total_weight}kg")

# --- Step 4: Engineering Viability Check ---
st.markdown("---")
st.subheader("⚙️ Engineering Compatibility Check")

viable = True
messages = []

# Get component types for easier checking
has_battery = any("Battery" in c["name"] for c in user_components)
has_inverter = any(c["name"] == "Inverter" for c in user_components)
has_controller = any("Controller" in c["name"] for c in user_components)
has_solar_panels = any("Solar panel" in c["name"] for c in user_components)
has_appliances = any(c.get("is_appliance", False) for c in user_components)

batteries = [c for c in user_components if "Battery" in c["name"]]
controllers = [c for c in user_components if "Controller" in c["name"]]
solar_panels = [c for c in user_components if "Solar panel" in c["name"]]
inverter = next((c for c in user_components if c["name"] == "Inverter"), None)
motor_attachments = [c for c in user_components if c["category"] == "Motor Attachments"]
cooker_accessories = [c for c in user_components if c["category"] == "Cooker Accessories"]
appliances = [c for c in user_components if c.get("is_appliance", False)]
iceboxes = [c for c in user_components if "icebox" in c["name"].lower()]

# --- Rule 1: AC Product with DC Components requires Inverter ---
if product_info["voltage"] == "AC" and (has_battery or has_appliances) and not has_inverter:
    viable = False
    messages.append("⚠️ AC product requires Inverter when using DC components like Battery or DC appliances")

# --- Rule 2: DC Product should not use Inverter ---
if product_info["voltage"] == "DC" and has_inverter:
    viable = False
    messages.append("⚠️ DC product cannot use Inverter (already DC-compatible)")

# --- Rule 3: Battery requires compatible Controller (unless battery includes one) ---
if has_battery and not has_controller:
    battery_with_controller = any(b.get("includes_controller", False) for b in batteries)
    if not battery_with_controller:
        viable = False
        messages.append("⚠️ Battery requires a Solar Controller for regulation")

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

# --- Rule 5: Total power calculation for appliances ---
total_appliance_power = sum(float(appliance.get("power_rating", 0)) for appliance in appliances) + product_info["power_watts"]
if has_controller:
    for controller in controllers:
        controller_power = float(controller.get("power_rating", 0))
        if total_appliance_power > controller_power:
            viable = False
            messages.append(f"⚠️ Total appliance power ({total_appliance_power}W) exceeds {controller['name']} max output ({controller_power}W)")

# --- Rule 6: Battery C-rating limits ---
for battery in batteries:
    battery_capacity = float(battery.get("battery_capacity", 0))
    battery_c_rating = float(battery.get("battery_c_rating", 1.0))
    max_battery_power = battery_capacity * battery_c_rating
    
    # Check total load against battery C-rating
    if total_appliance_power > max_battery_power:
        viable = False
        messages.append(f"⚠️ Total load ({total_appliance_power}W) exceeds {battery['name']} max discharge ({max_battery_power:.0f}W)")

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

# --- Step 5: Result ---
if not user_components:
    st.info("ℹ️ Add components to check engineering compatibility")
elif viable:
    st.success("✅ System is electrically compatible and power ratings are within limits.")
else:
    st.error("❌ Incompatible system configuration detected:")
    for msg in messages:
        st.markdown(f"- {msg}")

# --- Additional System Summary ---
if user_components:
    st.markdown("---")
    st.subheader("📊 Power System Summary")
    
    system_limits = {}
    
    if solar_panels:
        total_solar_power = sum(float(panel.get("power_rating", 0)) for panel in solar_panels)
        system_limits["Total Solar Power"] = f"{total_solar_power}Wp"
    
    if controllers:
        total_controller_power = sum(float(c.get("power_rating", 0)) for c in controllers)
        system_limits["Total Controller Capacity"] = f"{total_controller_power}W"
    
    if batteries:
        total_battery_capacity = sum(float(b.get("battery_capacity", 0)) for b in batteries)
        max_total_power = sum(float(b.get("battery_capacity", 0)) * float(b.get("battery_c_rating", 1.0)) for b in batteries)
        system_limits["Total Battery Capacity"] = f"{total_battery_capacity}Wh"
        system_limits["Max System Power"] = f"{max_total_power:.0f}W"
    
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
if user_components and viable:
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
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