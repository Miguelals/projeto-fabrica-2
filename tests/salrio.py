import streamlit as st

# 🌍 Mensagens multilíngue
mensagens = {
    "pt": {
        "titulo": "💼 Calculadora de Salário Mensal",
        "descricao": "Informe seus dados para calcular o salário bruto e líquido com base na carga horária.",
        "nome": "Nome do trabalhador:",
        "valor_hora": "Valor por hora (R$):",
        "modo": "Modo de entrada:",
        "opcao_mes": "Horas trabalhadas no mês",
        "opcao_semana": "Carga horária semanal",
        "horas_mes": "Horas trabalhadas no mês:",
        "horas_semana": "Horas semanais:",
        "botao": "Calcular salário",
        "resultado_bruto": "💰 Salário bruto:",
        "resultado_liquido": "🧾 Salário líquido:",
        "inss": "Desconto INSS (9%):",
        "ir": "Desconto IR (7.5% acima de R$ 2.500):",
        "erro_valor": "❌ Valor inválido. Digite um número positivo.",
        "erro_horas": "❌ Número de horas fora do intervalo permitido.",
        "idioma": "Idioma",
        "relatorio": "📄 Relatório detalhado",
        "copiar_info": "Abaixo estão os dados calculados. Você pode copiá-los para uso posterior.",
        "rodape": "Desenvolvido com ❤️ usando Streamlit."
    },
    "en": {
        "titulo": "💼 Monthly Salary Calculator",
        "descricao": "Enter your data to calculate gross and net salary based on working hours.",
        "nome": "Worker's name:",
        "valor_hora": "Hourly rate ($):",
        "modo": "Input mode:",
        "opcao_mes": "Monthly hours worked",
        "opcao_semana": "Weekly workload",
        "horas_mes": "Monthly hours:",
        "horas_semana": "Weekly hours:",
        "botao": "Calculate salary",
        "resultado_bruto": "💰 Gross salary:",
        "resultado_liquido": "🧾 Net salary:",
        "inss": "INSS deduction (9%):",
        "ir": "IR deduction (7.5% above $2,500):",
        "erro_valor": "❌ Invalid value. Enter a positive number.",
        "erro_horas": "❌ Number of hours outside allowed range.",
        "idioma": "Language",
        "relatorio": "📄 Detailed Report",
        "copiar_info": "Below are the calculated data. You can copy them for later use.",
        "rodape": "Developed with ❤️ using Streamlit."
    }
}

# 🧮 Funções de cálculo
def calcular_salario_bruto(valor_hora, horas):
    return valor_hora * horas

def calcular_descontos(salario_bruto):
    inss = salario_bruto * 0.09
    ir = (salario_bruto - 2500) * 0.075 if salario_bruto > 2500 else 0
    return inss, ir

def calcular_salario_liquido(salario_bruto, inss, ir):
    return salario_bruto - inss - ir

# 🚀 App principal
def main():
    st.set_page_config(page_title="Calculadora de Salário", page_icon="💼", layout="wide")

    idioma = st.sidebar.selectbox("🌐 Idioma / Language", ["pt", "en"])
    msgs = mensagens[idioma]

    st.title(msgs["titulo"])
    st.markdown(f"#### {msgs['descricao']}")

    # Abas para separar entrada e relatório
    aba1, aba2 = st.tabs([msgs["botao"], msgs["relatorio"]])

    with aba1:
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input(msgs["nome"])
        with col2:
            valor_hora = st.number_input(msgs["valor_hora"], min_value=0.0, format="%.2f")

        modo = st.radio(msgs["modo"], [msgs["opcao_mes"], msgs["opcao_semana"]])
        if modo == msgs["opcao_mes"]:
            horas = st.number_input(msgs["horas_mes"], min_value=0.0, max_value=744.0, format="%.2f")
        else:
            horas_semana = st.number_input(msgs["horas_semana"], min_value=0.0, max_value=168.0, format="%.2f")
            horas = horas_semana * 4.5

        if st.button(msgs["botao"]):
            if valor_hora > 0 and horas > 0:
                bruto = calcular_salario_bruto(valor_hora, horas)
                inss, ir = calcular_descontos(bruto)
                liquido = calcular_salario_liquido(bruto, inss, ir)

                st.success("✅ Cálculo realizado com sucesso!")

                st.subheader(msgs["resultado_bruto"])
                st.write(f"R$ {bruto:.2f}" if idioma == "pt" else f"$ {bruto:.2f}")

                st.subheader(msgs["resultado_liquido"])
                st.write(f"R$ {liquido:.2f}" if idioma == "pt" else f"$ {liquido:.2f}")

                # Salvar os dados em sessão
                st.session_state["dados"] = {
                    "nome": nome,
                    "valor_hora": valor_hora,
                    "horas": horas,
                    "bruto": bruto,
                    "inss": inss,
                    "ir": ir,
                    "liquido": liquido
                }
            else:
                st.error(msgs["erro_valor"])

    with aba2:
        if "dados" in st.session_state:
            dados = st.session_state["dados"]
            st.markdown("### 📊 " + msgs["relatorio"])
            st.info(msgs["copiar_info"])
            st.markdown("---")

            st.markdown(f"""
            **👷 Nome:** {dados["nome"]}  
            **💸 Valor por hora:** R$ {dados["valor_hora"]:.2f}  
            **⏱️ Horas no mês:** {dados["horas"]:.2f}  
            **💰 Salário bruto:** R$ {dados["bruto"]:.2f}  
            **🧾 INSS (9%):** R$ {dados["inss"]:.2f}  
            **💵 IR (7.5% acima de R$ 2500):** R$ {dados["ir"]:.2f}  
            **🟢 Salário líquido:** R$ {dados["liquido"]:.2f}
            """)
        else:
            st.warning("⚠️ Nenhum cálculo realizado ainda.")

    st.markdown("---")
    st.caption(msgs["rodape"])

if __name__ == "__main__":
    main()
